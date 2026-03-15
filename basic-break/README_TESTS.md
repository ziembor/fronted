# Break Timer - Playwright Tests

## Overview

Comprehensive end-to-end test suite for the Training Break Timer application using Playwright. The suite includes 24 tests covering all major functionality.

## Prerequisites

- **Python**: 3.13+ (tested with Python 3.13.11)
- **Operating System**: Windows, macOS, or Linux
- **Browsers**: Chromium (automatically installed by Playwright)

## Setup

### 1. Install Python Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or install individual packages:
```bash
pip install pytest pytest-playwright playwright --upgrade
```

**Dependencies:**
- `pytest` (9.0.2+) - Test framework
- `pytest-playwright` (0.7.2+) - Playwright plugin for pytest
- `playwright` (1.58.0+) - Browser automation library

### 2. Install Playwright Browsers

Install Chromium browser binaries:
```bash
python -m playwright install
```

Or install only Chromium (faster):
```bash
python -m playwright install chromium
```

## Running Tests

### Basic Test Execution

Run all tests with verbose output:
```bash
python -m pytest test_break_timer.py -v
```

Run a specific test:
```bash
python -m pytest test_break_timer.py::test_quick_time_15_minutes -v
```

Run tests matching a pattern:
```bash
python -m pytest test_break_timer.py -k "toggle" -v
```

### Visual Testing Options

Run tests with visible browser (headed mode):
```bash
python -m pytest test_break_timer.py -v --headed
```

Run tests with slow motion (1 second delay per action):
```bash
python -m pytest test_break_timer.py -v --headed --slowmo 1000
```

Run tests with browser DevTools open:
```bash
python -m pytest test_break_timer.py -v --headed --devtools
```

### Advanced Options

Run tests in parallel (faster execution):
```bash
python -m pytest test_break_timer.py -v -n auto
```

Generate HTML report:
```bash
python -m pytest test_break_timer.py -v --html=report.html --self-contained-html
```

Run with detailed output:
```bash
python -m pytest test_break_timer.py -vv
```

Stop at first failure:
```bash
python -m pytest test_break_timer.py -v -x
```

## Test Coverage

### Summary
- **Total Tests**: 24
- **Success Rate**: 100% (all passing)
- **Execution Time**: ~19 seconds (headless mode)
- **Browsers Tested**: Chromium

### Test Categories

#### 1. Page Loading & UI (3 tests)
- `test_page_loads` - Verifies page loads with correct title and heading
- `test_ui_elements_present` - Checks all UI elements are present and visible
- `test_timezone_selector_present` - Validates timezone selector has 14 options

#### 2. Timer Configuration (7 tests)
- `test_quick_time_15_minutes` - Tests +15 minutes quick button
- `test_quick_time_30_minutes` - Tests +30 minutes quick button
- `test_next_full_hour` - Tests "Next Full Hour" button
- `test_next_quarter_hour` - Tests "Next :15 After Hour" button
- `test_custom_minutes_input` - Tests custom minutes input field
- `test_specific_datetime_input` - Tests specific datetime picker
- `test_invalid_time_alert` - Tests error handling for invalid times

#### 3. Time Display & Format (3 tests)
- `test_time_displays_iso_format` - Validates ISO 8601 format without seconds
- `test_current_times_update` - Verifies time displays update every second
- `test_countdown_updates` - Checks countdown timer decrements properly

#### 4. Timezone Functionality (5 tests)
- `test_default_timezones_displayed` - Verifies UTC and CET/CEST always shown
- `test_additional_timezone_selection` - Tests selecting one additional timezone
- `test_multiple_timezone_selection` - Tests selecting multiple timezones (3+)
- `test_timezone_times_update` - Verifies all timezone displays update
- `test_reset_clears_timezone_selection` - Checks reset clears timezone selection

#### 5. Toggle Switches (5 tests)
- `test_show_seconds_toggle_default` - Verifies "Show Seconds" is disabled by default
- `test_show_seconds_enabled` - Tests enabling seconds display (ISO format with seconds)
- `test_play_sound_toggle_default` - Verifies "Play Sound" is disabled by default
- `test_play_sound_toggle_exists` - Tests enabling sound toggle
- `test_reset_clears_toggles` - Verifies reset clears both toggles

#### 6. Reset Functionality (1 test)
- `test_reset_button` - Tests complete reset flow (timer → setup screen)

### Detailed Feature Coverage

✅ **Timer Configuration**
- Quick time options (15 min, 30 min, next hour, next quarter)
- Custom duration input
- Specific end time picker
- Input validation and error handling

✅ **Time Display**
- ISO 8601 format: `YYYY-MM-DD HH:MM` (default)
- ISO 8601 format with seconds: `YYYY-MM-DD HH:MM:SS` (when enabled)
- End time display
- Real-time countdown
- Multi-timezone current time displays

✅ **Timezone Support**
- Default timezones (UTC, CET/CEST)
- 14 selectable timezones
- Multiple timezone selection (Ctrl+Click)
- Timezone label mapping
- Real-time timezone updates

✅ **Toggle Functionality**
- Show Seconds toggle (on/off)
- Play Sound toggle (on/off)
- Toggle state persistence during timer
- Toggle reset on new timer

✅ **User Interface**
- Screen transitions (setup ↔ timer)
- Button states and interactions
- Input field behavior
- Responsive layout
- Color-coded countdown warnings

✅ **Reset & State Management**
- Clear all inputs
- Reset timezones
- Reset toggles
- Return to setup screen
- Clear timer state

## Test Implementation Notes

### Custom Toggle Styling
The toggle switches use custom CSS styling with `opacity: 0` on the actual checkbox elements. Tests interact with the visible `.toggle-slider` elements instead:

```python
# Click the visible slider, not the hidden checkbox
page.locator('label:has(#showSeconds) .toggle-slider').click()
```

### Time Update Tests
Tests that verify time updates enable "Show Seconds" first, since the default format `YYYY-MM-DD HH:MM` only changes once per minute:

```python
# Enable seconds to see updates within 2 seconds
page.locator('label:has(#showSeconds) .toggle-slider').click()
page.wait_for_timeout(2000)  # Now we can verify seconds changed
```

### Browser Compatibility
Tests run against Chromium by default. Playwright also supports:
- Firefox (add `--browser firefox`)
- WebKit (add `--browser webkit`)

Run tests on all browsers:
```bash
python -m pytest test_break_timer.py -v --browser chromium --browser firefox --browser webkit
```

## Troubleshooting

### Common Issues

**Issue**: `pytest: command not found`
```bash
# Solution: Use python -m pytest instead
python -m pytest test_break_timer.py -v
```

**Issue**: `ModuleNotFoundError: No module named 'playwright'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Browser binaries not found
```bash
# Solution: Install Playwright browsers
python -m playwright install
```

**Issue**: Tests fail on Python 3.13
```bash
# Solution: Upgrade to latest versions
pip install pytest pytest-playwright playwright --upgrade
```

**Issue**: `Element is outside of the viewport`
```bash
# This is expected for hidden toggle checkboxes
# Tests use .toggle-slider instead (already fixed in tests)
```

## Test Maintenance

### Adding New Tests

1. Follow existing test patterns
2. Use descriptive test names: `test_<feature>_<scenario>`
3. Add docstrings explaining what the test validates
4. Update this README with new test coverage
5. Ensure tests are independent (no shared state)

### Best Practices

- **Isolation**: Each test starts fresh (no dependencies between tests)
- **Clarity**: Clear test names and docstrings
- **Assertions**: Use Playwright's `expect()` for better error messages
- **Waits**: Use explicit waits (`wait_for_timeout`) when needed
- **Selectors**: Prefer semantic selectors (IDs, test IDs) over CSS selectors
- **Force Actions**: Only use `force=True` when absolutely necessary (e.g., hidden elements)

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install chromium
      - name: Run tests
        run: python -m pytest test_break_timer.py -v
```

## Test Results

Latest test run (2026-03-03):
```
============================= 24 passed in 19.06s =============================
```

- ✅ All 24 tests passing
- 🚀 Execution time: 19.06 seconds
- 🌐 Browser: Chromium
- 💯 Success rate: 100%

## Future Test Enhancements

Potential additions for comprehensive coverage:

- [ ] Visual regression tests (screenshot comparison)
- [ ] Audio playback verification
- [ ] Browser notification tests
- [ ] Performance/memory leak tests
- [ ] Accessibility (a11y) tests
- [ ] Mobile/responsive layout tests
- [ ] Cross-browser compatibility tests
- [ ] Edge case testing (very long timers, timezone edge cases)
- [ ] Keyboard navigation tests
- [ ] Test coverage reporting

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-playwright Plugin](https://github.com/microsoft/playwright-pytest)
