#ifndef CANINANA_CORE_INCLUDE_PERFORMANCE_MONITOR_H_
#define CANINANA_CORE_INCLUDE_PERFORMANCE_MONITOR_H_

#include <chrono>

namespace caninana {
namespace core {

/**
 * @class PerformanceMonitor
 * @brief A simple utility to track elapsed time for performance-sensitive
 * operations.
 *
 * This class provides a high-precision timer to enforce timeouts, preventing
 * denial-of-service vulnerabilities from scans that run for too long.
 */
class PerformanceMonitor {
 public:
  /**
   * @brief Starts the timer, capturing the current time point.
   */
  void Start();

  /**
   * @brief Checks if the specified timeout duration has elapsed since Start()
   * was called.
   * @param timeout The maximum duration allowed for the operation.
   * @return True if the elapsed time is greater than or equal to the timeout,
   * false otherwise.
   */
  bool HasTimedOut(std::chrono::seconds timeout) const;

 private:
  /// The time point when the monitor was started.
  std::chrono::steady_clock::time_point start_time_;
};

}  // namespace core
}  // namespace caninana

#endif  // CANINANA_CORE_INCLUDE_PERFORMANCE_MONITOR_H_