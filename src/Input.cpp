#include "Globals.hpp"
#include "Overview.hpp"

#include <cmath>

#include <hyprland/src/desktop/view/Window.hpp>

// 컴পাইলারের Deprecation Warning ইগনোর করার জন্য প্রাগমা যুক্ত করা হলো
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

namespace {

double panelTravel(PHLMONITOR owner) {
  if (!owner)
    return 0.;

  return (Config::panelHeight + Config::reservedArea) * owner->m_scale;
}

double swipeClosedOffset() { return -Config::swipeClosedPadding; }

double swipeVisibleThreshold() { return Config::swipeThreshold; }

} // namespace

bool CHyprspaceWidget::buttonEvent(bool pressed, Vector2D coords) {
  bool Return;

  const auto dragTarget = g_layoutManager->dragController()->target();
  const auto targetWindow = dragTarget ? dragTarget->window() : nullptr;

  // this is for click to exit, we set a timeout for button release
  bool couldExit = false;
  if (pressed)
    lastPressedTime = std::chrono::high_resolution_clock::now();
  else if (std::chrono::duration_cast<std::chrono::milliseconds>(
               std::chrono::high_resolution_clock::now() - lastPressedTime)
               .count() < Config::clickReleaseThresholdMs)
    couldExit = true;

  int targetWorkspaceID = SPECIAL_WORKSPACE_START - 1;

  // find which workspace the mouse hovers over
  for (auto &w : workspaceBoxes) {
    auto wi = std::get<0>(w);
    auto wb = std::get<1>(w);
    if (wb.containsPoint(coords)) {
      targetWorkspaceID = wi;
      break;
    }
  }

  auto targetWorkspace = g_pCompositor->getWorkspaceByID(targetWorkspaceID);

  // create new workspace
  if (targetWorkspace == nullptr &&
      targetWorkspaceID >= SPECIAL_WORKSPACE_START) {
    targetWorkspace =
        g_pCompositor->createNewWorkspace(targetWorkspaceID, getOwner()->m_id);
  }

  // if the cursor is hovering over workspace, clicking should switch workspace
  // instead of starting window drag
  if (Config::autoDrag && (targetWorkspace == nullptr || !pressed)) {
    if (g_layoutManager->dragController()->target())
      g_layoutManager->endDragTarget();

    if (pressed) {
      const auto PWINDOW = g_pCompositor->vectorToWindowUnified(
          coords, Desktop::View::WINDOW_ONLY, nullptr);
      if (PWINDOW) {
        const auto LT = PWINDOW->layoutTarget();
        if (LT)
          g_layoutManager->beginDragTarget(LT, MBIND_MOVE);
      }
    }
  }
  Return = false;

  // release window on workspace to drop it in
  if (targetWindow && targetWorkspace != nullptr && !pressed) {
    g_pCompositor->moveWindowToWorkspaceSafe(targetWindow, targetWorkspace);
    if (targetWindow->m_isFloating) {
      auto targetPos = getOwner()->m_position + (getOwner()->m_size / 2.) -
                       (targetWindow->m_reportedSize / 2.);
      targetWindow->m_position = targetPos;
      *targetWindow->m_realPosition = targetPos;
    }
    if (Config::switchOnDrop) {
      g_pCompositor->getMonitorFromID(targetWorkspace->m_monitor->m_id)
          ->changeWorkspace(targetWorkspace->m_id);
      if (Config::exitOnSwitch && active)
        hide();
    }
    updateLayout();
  }
  // click workspace to change to workspace and exit overview
  else if (targetWorkspace && !pressed) {
    if (targetWorkspace->m_isSpecialWorkspace)
      getOwner()->activeSpecialWorkspaceID() == targetWorkspaceID
          ? getOwner()->setSpecialWorkspace(nullptr)
          : getOwner()->setSpecialWorkspace(targetWorkspaceID);
    else {
      g_pCompositor->getMonitorFromID(targetWorkspace->m_monitor->m_id)
          ->changeWorkspace(targetWorkspace->m_id);
    }
    if (Config::exitOnSwitch && active)
      hide();
  }
  // click elsewhere to exit overview
  else if (Config::exitOnClick && targetWorkspace == nullptr && active &&
           couldExit && !pressed)
    hide();

  return Return;
}

bool CHyprspaceWidget::axisEvent(double delta, wl_pointer_axis axis,
                                 Vector2D coords) {

  const auto owner = getOwner();
  const auto travel = panelTravel(owner);
  CBox widgetBox = {owner->m_position.x,
                    owner->m_position.y - curYOffset->value(),
                    owner->m_transformedSize.x, travel};
  if (Config::onBottom)
    widgetBox = {owner->m_position.x,
                 owner->m_position.y + owner->m_transformedSize.y - travel +
                     curYOffset->value(),
                 owner->m_transformedSize.x, travel};

  // scroll through panel if cursor is on it
  if (widgetBox.containsPoint(coords * getOwner()->m_scale)) {
    // only horizontal scroll pans the panel; ignore vertical scroll here
    if (axis == WL_POINTER_AXIS_HORIZONTAL_SCROLL)
      *workspaceScrollOffset =
          workspaceScrollOffset->goal() - delta * Config::workspaceScrollSpeed;
  }
  // otherwise, scroll to switch active workspace (vertical scroll only)
  else if (Config::autoScroll && axis == WL_POINTER_AXIS_VERTICAL_SCROLL) {
    if (delta < 0) {
      SWorkspaceIDName wsIDName = getWorkspaceIDNameFromString("r-1");
      if (g_pCompositor->getWorkspaceByID(wsIDName.id) == nullptr) {
        auto newWorkspace =
            g_pCompositor->createNewWorkspace(wsIDName.id, ownerID);
        (void)newWorkspace;
      }
      getOwner()->changeWorkspace(wsIDName.id);
    } else {
      SWorkspaceIDName wsIDName = getWorkspaceIDNameFromString("r+1");
      if (g_pCompositor->getWorkspaceByID(wsIDName.id) == nullptr) {
        auto newWorkspace =
            g_pCompositor->createNewWorkspace(wsIDName.id, ownerID);
        (void)newWorkspace;
      }
      getOwner()->changeWorkspace(wsIDName.id);
    }
  }

  return false;
}

bool CHyprspaceWidget::isSwiping() { return swiping; }

bool CHyprspaceWidget::beginSwipe(IPointer::SSwipeBeginEvent e) {
  swiping = true;
  activeBeforeSwipe = active;
  avgSwipeSpeed = 0;
  swipePoints = 0;
  return false;
}

bool CHyprspaceWidget::updateSwipe(IPointer::SSwipeUpdateEvent e) {
  // restrict swipe to a axis with the most significant movement to prevent
  // misinput
  const auto absY = std::abs(e.delta.y);
  const auto verticalSwipe = absY > 0.0 && (std::abs(e.delta.x) / absY) < 1.0;

  if (verticalSwipe) {
    if (swiping && e.fingers == static_cast<uint32_t>(Config::swipeFingers)) {

      const auto owner = getOwner();
      if (!owner)
        return true;

      const auto distance = std::max(Config::swipeDistance, 1);
      const auto currentScaling =
          owner->m_size.x / static_cast<float>(distance);
      const auto travel = panelTravel(owner);

      double scrollDifferential = e.delta.y * (Config::reverseSwipe ? -1 : 1) *
                                  (Config::onBottom ? -1 : 1) * currentScaling;

      curSwipeOffset += scrollDifferential;
      curSwipeOffset =
          std::clamp<double>(curSwipeOffset, swipeClosedOffset(), travel);

      avgSwipeSpeed = (avgSwipeSpeed * swipePoints + scrollDifferential) /
                      (swipePoints + 1);
      swipePoints++;

      curYOffset->setValueAndWarp(travel - curSwipeOffset);

      if (curSwipeOffset < swipeVisibleThreshold() && active)
        hide();
      else if (curSwipeOffset > swipeVisibleThreshold() && !active)
        show();

      return false;
    }
  } else {
    // scroll through panel
    if (e.fingers == static_cast<uint32_t>(Config::swipeFingers) && active) {
      const auto owner = getOwner();
      const auto travel = panelTravel(owner);
      CBox widgetBox = {owner->m_position.x,
                        owner->m_position.y - curYOffset->value(),
                        owner->m_transformedSize.x, travel};
      if (Config::onBottom)
        widgetBox = {owner->m_position.x,
                     owner->m_position.y + owner->m_transformedSize.y - travel +
                         curYOffset->value(),
                     owner->m_transformedSize.x, travel};
      if (widgetBox.containsPoint(g_pInputManager->getMouseCoordsInternal() *
                                  getOwner()->m_scale)) {
        workspaceScrollOffset->setValueAndWarp(
            workspaceScrollOffset->goal() +
            e.delta.x * Config::workspaceScrollSpeed);
        return false;
      }
    }
  }
  // otherwise, do not cancel the event and perform workspace swipe normally
  return true;
}

// janky asf
bool CHyprspaceWidget::endSwipe(IPointer::SSwipeEndEvent e) {
  swiping = false;
  const auto owner = getOwner();
  const auto travel = panelTravel(owner);
  // force cancel swipe
  if (e.cancelled) {
    if (active)
      hide();
    curSwipeOffset = swipeClosedOffset();
  } else {
    if (activeBeforeSwipe) {
      if ((curSwipeOffset < travel * Config::swipeCancelRatio) ||
          avgSwipeSpeed < -Config::swipeForceSpeed) {
        if (active)
          hide();
        else {
          *curYOffset = travel;
          curSwipeOffset = swipeClosedOffset();
        }
      } else {
        // cancel
        if (!active)
          show();
        else {
          *curYOffset = 0;
          curSwipeOffset = travel;
        }
      }
    } else {
      if ((curSwipeOffset > travel * (1.F - Config::swipeCancelRatio)) ||
          avgSwipeSpeed > Config::swipeForceSpeed) {
        if (!active)
          show();
        else {
          *curYOffset = 0;
          curSwipeOffset = travel;
        }
      } else {
        // cancel
        if (active)
          hide();
        else {
          *curYOffset = travel;
          curSwipeOffset = swipeClosedOffset();
        }
      }
    }
  }
  avgSwipeSpeed = 0;
  swipePoints = 0;
  return false;
}
