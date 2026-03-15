# Training Break Timer

A self-contained, single-page web application for managing training breaks with multi-timezone support. Perfect for remote teams, distributed training sessions, or anyone needing to coordinate break times across different time zones.

## Features

### Timer Configuration
- **Quick Time Options**
  - +15 Minutes
  - +30 Minutes
  - Next Full Hour
  - Next Quarter Hour (:15 after current or next hour)
- **Custom Duration** - Set any number of minutes
- **Specific End Time** - Pick exact date and time using datetime picker

### Display Options
- **Show Seconds Toggle** - Enable/disable seconds display (default: disabled)
- **Play Sound Toggle** - Enable/disable school bell sound at timer completion (default: disabled)
- **Multi-Timezone Display** - Always shows UTC and CET/CEST, plus 14 additional selectable timezones

### Timer Features
- **Real-time Countdown** - Updates every second
- **Color-coded Warnings**
  - Normal: Purple/Blue
  - Warning: Orange (< 5 minutes remaining)
  - Urgent: Red (< 1 minute remaining)
- **Browser Notifications** - Desktop notification when timer completes
- **School Bell Sound** - Three-tone bell pattern using Web Audio API

### Time Format
- **ISO 8601 Standard** - All times displayed as `YYYY-MM-DD HH:MM` or `YYYY-MM-DD HH:MM:SS`
- **Consistent Formatting** - Same format for end time and all timezone displays

## Code Structure

### Architecture
```
index.html (527 lines)
├── CSS Styles (lines 7-284)
│   ├── Layout & Container Styles
│   ├── Input & Button Styles
│   ├── Timer Display Styles
│   ├── Toggle Switch Styles
│   └── Responsive Design
├── HTML Structure (lines 285-369)
│   ├── Setup Screen
│   │   ├── Quick Time Buttons
│   │   ├── Custom Input Fields
│   │   ├── Timezone Selector
│   │   ├── Show Seconds Toggle
│   │   ├── Play Sound Toggle
│   │   └── Start Button
│   └── Timer Screen
│       ├── End Time Display
│       ├── Countdown Timer
│       ├── Finished Message
│       ├── Current Times (Multi-timezone)
│       └── Reset Button
└── JavaScript (lines 371-670)
    ├── Global State Variables
    ├── Timer Configuration Functions
    ├── Display Setup Functions
    ├── Audio Generation Function
    ├── Timer Update Logic
    └── Reset Function
```

### Global State Variables

```javascript
let endTime = null;              // Date object for timer end time
let timerInterval = null;        // setInterval reference for countdown
let selectedTimezones = [];      // Array of timezone strings
let showSeconds = false;         // Boolean for seconds display
let playSound = false;           // Boolean for sound playback
```

## Functions Documentation

### Timer Configuration Functions

#### `setQuickTime(minutes)`
**Location:** `index.html:377-382`
**Purpose:** Sets end time to current time + specified minutes
**Parameters:**
- `minutes` (number) - Number of minutes to add

**Example:**
```javascript
setQuickTime(15);  // Sets timer to 15 minutes from now
```

#### `setNextFullHour()`
**Location:** `index.html:384-394`
**Purpose:** Sets end time to the next full hour (XX:00:00)
**Logic:**
- Adds 1 hour to current time
- Sets minutes, seconds, milliseconds to 0

#### `setNextQuarter()`
**Location:** `index.html:396-415`
**Purpose:** Sets end time to next :15 mark after the hour
**Logic:**
- If current time is before :15 → sets to :15 of current hour
- Otherwise → sets to :15 of next hour

### Timer Control Functions

#### `startTimer()`
**Location:** `index.html:417-471`
**Purpose:** Validates input, initializes timer, switches to timer screen
**Process:**
1. Reads custom minutes input (if provided)
2. Reads specific datetime input (if provided)
3. Validates end time is in the future
4. Collects selected timezones (defaults: UTC, Europe/Paris)
5. Reads toggle preferences (showSeconds, playSound)
6. Sets up timezone displays
7. Switches to timer screen
8. Starts countdown interval (1-second updates)

**Validation:**
- Shows alert if no valid end time selected
- Ensures end time is in the future

#### `resetTimer()`
**Location:** `index.html:652-666`
**Purpose:** Clears timer state and returns to setup screen
**Actions:**
- Clears interval
- Resets all state variables
- Switches to setup screen
- Clears all input fields
- Unchecks all toggles

### Display Functions

#### `setupTimezoneDisplays()`
**Location:** `index.html:473-521`
**Purpose:** Dynamically creates timezone display elements
**Process:**
1. Clears existing container
2. For each selected timezone:
   - Creates display element
   - Adds timezone label
   - Adds time value placeholder
   - Appends to container

**Timezone Labels:**
```javascript
{
  'UTC': 'UTC',
  'Europe/Paris': 'CET/CEST',
  'America/New_York': 'EST/EDT',
  // ... 11 more timezones
}
```

#### `updateEndTimeDisplay()`
**Location:** `index.html:523-541`
**Purpose:** Formats and displays the timer end time
**Format:**
- With seconds: `YYYY-MM-DD HH:MM:SS`
- Without seconds: `YYYY-MM-DD HH:MM`

#### `updateTimer()`
**Location:** `index.html:543-650`
**Purpose:** Main timer loop - updates all displays every second
**Process:**
1. Calculate time difference
2. Update all timezone displays using `Intl.DateTimeFormat`
3. Update countdown timer
4. Apply color coding based on remaining time
5. Handle timer completion:
   - Display "00:00:00"
   - Show finished message
   - Play sound (if enabled)
   - Send browser notification (if permitted)
   - Clear interval

**Color Coding Logic:**
- `diff < 60000ms` (< 1 min) → Urgent (red)
- `diff < 300000ms` (< 5 min) → Warning (orange)
- Otherwise → Normal (purple/blue)

**Timezone Conversion:**
Uses `Intl.DateTimeFormat.formatToParts()` for accurate timezone conversion:
```javascript
const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',  // Only if showSeconds is true
    hour12: false
});
```

### Audio Functions

#### `playSchoolBell()`
**Location:** `index.html:523-549`
**Purpose:** Generates and plays school bell sound using Web Audio API
**Pattern:** Three-tone sequence (High-Low-High)
- Tone 1: 800Hz at 0.0s
- Tone 2: 660Hz at 0.3s
- Tone 3: 800Hz at 0.6s

**Envelope:**
- Quick attack: 0 → 0.3 gain in 0.01s
- Exponential decay: 0.3 → 0.01 gain over 0.5s
- Total duration per bell: 0.5s

## Supported Timezones

### Always Displayed
- **UTC** - Coordinated Universal Time
- **CET/CEST** - Central European Time (Europe/Paris)

### Selectable (14 options)
- **EST/EDT** - Eastern Time (America/New_York)
- **CST/CDT** - Central Time (America/Chicago)
- **MST/MDT** - Mountain Time (America/Denver)
- **PST/PDT** - Pacific Time (America/Los_Angeles)
- **GMT/BST** - Greenwich Mean Time (Europe/London)
- **CET/CEST** - Central European Time (Europe/Berlin)
- **MSK** - Moscow Time (Europe/Moscow)
- **GST** - Gulf Standard Time (Asia/Dubai)
- **IST** - India Standard Time (Asia/Kolkata)
- **CST** - China Standard Time (Asia/Shanghai)
- **JST** - Japan Standard Time (Asia/Tokyo)
- **KST** - Korea Standard Time (Asia/Seoul)
- **AEDT/AEST** - Australian Eastern Time (Australia/Sydney)
- **NZDT/NZST** - New Zealand Time (Pacific/Auckland)

## Usage

### Basic Usage
1. Open `index.html` in any modern web browser
2. Select timer duration using one of the methods:
   - Click a quick option button (+15 min, +30 min, etc.)
   - Enter custom minutes
   - Pick specific end time
3. (Optional) Select additional timezones to display
4. (Optional) Enable "Show Seconds" toggle
5. (Optional) Enable "Play Sound at End" toggle
6. Click "Start Break Timer"
7. Monitor countdown and timezone displays
8. Click "New Break Timer" to reset

### Advanced Usage

#### Multiple Timezones
1. Hold Ctrl (Windows/Linux) or Cmd (Mac)
2. Click multiple timezones in the selector
3. All selected timezones will display during countdown

#### Notifications
- Browser will request notification permission on first load
- Grant permission to receive desktop notifications when timer completes

## Testing

### Test Suite
Comprehensive Playwright test suite with 24 tests covering:
- Page loading and UI elements
- All timer configuration methods
- Time format validation (with/without seconds)
- Countdown functionality
- Timezone selection and display
- Toggle switch functionality
- Reset functionality
- Error handling

### Running Tests

#### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

#### Run Tests
```bash
# All tests
pytest test_break_timer.py -v

# Specific test
pytest test_break_timer.py::test_show_seconds_enabled -v

# With visible browser
pytest test_break_timer.py -v --headed

# Slow motion for debugging
pytest test_break_timer.py -v --headed --slowmo 1000
```

### Test Coverage
- ✅ 24 total tests
- ✅ 100% feature coverage
- ✅ Time format validation
- ✅ Toggle functionality
- ✅ Multi-timezone support
- ✅ Error handling
- ✅ Reset functionality

## Technical Details

### Dependencies
- **None** - Completely self-contained
- No external libraries, frameworks, or CDNs
- Pure HTML5, CSS3, and vanilla JavaScript

### Browser Compatibility
- Modern browsers supporting:
  - `Intl.DateTimeFormat` API
  - Web Audio API
  - Notifications API
  - CSS Grid and Flexbox
  - ES6+ JavaScript

### Performance
- Minimal resource usage
- 1-second update interval
- Efficient DOM manipulation
- No memory leaks (proper interval cleanup)

### Security
- ✅ No external dependencies
- ✅ No data collection
- ✅ No server communication
- ✅ No XSS vulnerabilities
- ✅ No innerHTML usage
- ✅ Runs entirely client-side

## File Structure

```
basic-break/
├── index.html              # Main application (self-contained)
├── test_break_timer.py     # Playwright test suite
├── requirements.txt        # Python test dependencies
├── README_TESTS.md        # Testing documentation
├── README.md              # This file
└── TODO.md                # Future enhancements and tasks
```

## License

This project is provided as-is for educational and practical use.

## Contributing

See `TODO.md` for planned improvements and enhancement opportunities.
