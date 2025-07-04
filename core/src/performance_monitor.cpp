#include "performance_monitor.h"

namespace caninana {
namespace core {

void PerformanceMonitor::Start() {
  start_time_ = std::chrono::steady_clock::now();
}

bool PerformanceMonitor::HasTimedOut(std::chrono::seconds timeout) const {
  const auto now = std::chrono::steady_clock::now();
  const auto elapsed =
      std::chrono::duration_cast<std::chrono::seconds>(now - start_time_);
  return elapsed >= timeout;
}

}  // namespace core
}  // namespace caninana