import pytest
import re
from datetime import datetime, timedelta
from playwright.sync_api import Page, expect
import os


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser to allow notifications"""
    return {
        **browser_context_args,
        "permissions": ["notifications"],
    }


@pytest.fixture
def page_url():
    """Get the absolute path to the HTML file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")
    return f"file:///{html_path.replace(os.sep, '/')}"


def test_page_loads(page: Page, page_url):
    """Test that the page loads correctly"""
    page.goto(page_url)

    # Check title
    expect(page).to_have_title("Training Break Timer")

    # Check main heading
    heading = page.locator("h1")
    expect(heading).to_have_text("Training Break Timer")

    # Check setup screen is visible
    setup_screen = page.locator(".setup-screen.active")
    expect(setup_screen).to_be_visible()


def test_quick_time_15_minutes(page: Page, page_url):
    """Test the +15 Minutes quick button"""
    page.goto(page_url)

    # Click +15 Minutes button
    page.click("text=+15 Minutes")

    # Click Start Break Timer
    page.click("text=Start Break Timer")

    # Timer screen should be visible
    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()

    # Check that time remaining is displayed
    time_remaining = page.locator("#timeRemaining")
    expect(time_remaining).not_to_have_text("--:--:--")

    # Check that end time is displayed in ISO format without seconds (YYYY-MM-DD HH:MM)
    end_time_display = page.locator("#endTimeDisplay")
    iso_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
    expect(end_time_display).to_have_text(re.compile(iso_pattern))


def test_quick_time_30_minutes(page: Page, page_url):
    """Test the +30 Minutes quick button"""
    page.goto(page_url)

    page.click("text=+30 Minutes")
    page.click("text=Start Break Timer")

    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()

    time_remaining = page.locator("#timeRemaining")
    expect(time_remaining).not_to_have_text("--:--:--")


def test_next_full_hour(page: Page, page_url):
    """Test the Next Full Hour button"""
    page.goto(page_url)

    page.click("text=Next Full Hour")
    page.click("text=Start Break Timer")

    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()

    # End time should show :00 for full hour (no seconds by default)
    end_time_display = page.locator("#endTimeDisplay")
    expect(end_time_display).to_contain_text(":00")


def test_next_quarter_hour(page: Page, page_url):
    """Test the Next :15 After Hour button"""
    page.goto(page_url)

    page.click("text=Next :15 After Hour")
    page.click("text=Start Break Timer")

    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()

    # End time should show :15 (no seconds by default)
    end_time_display = page.locator("#endTimeDisplay")
    expect(end_time_display).to_contain_text(":15")


def test_custom_minutes_input(page: Page, page_url):
    """Test custom minutes input"""
    page.goto(page_url)

    # Enter 5 minutes
    custom_input = page.locator("#customMinutes")
    custom_input.fill("5")

    page.click("text=Start Break Timer")

    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()

    time_remaining = page.locator("#timeRemaining")
    expect(time_remaining).not_to_have_text("--:--:--")


def test_specific_datetime_input(page: Page, page_url):
    """Test specific datetime input"""
    page.goto(page_url)

    # Set time to 30 minutes from now
    future_time = datetime.now() + timedelta(minutes=30)
    datetime_str = future_time.strftime("%Y-%m-%dT%H:%M")

    specific_time_input = page.locator("#specificTime")
    specific_time_input.fill(datetime_str)

    page.click("text=Start Break Timer")

    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()


def test_time_displays_iso_format(page: Page, page_url):
    """Test that all time displays use ISO 8601 format without seconds by default"""
    page.goto(page_url)

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Wait a moment for times to update
    page.wait_for_timeout(1000)

    # Check end time format (should not have seconds)
    end_time = page.locator("#endTimeDisplay")
    iso_pattern_no_seconds = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
    expect(end_time).to_have_text(re.compile(iso_pattern_no_seconds))

    # Check UTC time format (always displayed, no seconds)
    utc_time = page.locator("#time-UTC")
    expect(utc_time).to_have_text(re.compile(iso_pattern_no_seconds))

    # Check CET/CEST time format (always displayed, no seconds)
    cet_time = page.locator("#time-Europe-Paris")
    expect(cet_time).to_have_text(re.compile(iso_pattern_no_seconds))


def test_countdown_updates(page: Page, page_url):
    """Test that countdown timer updates"""
    page.goto(page_url)

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    time_remaining = page.locator("#timeRemaining")

    # Get initial value
    initial_text = time_remaining.text_content()

    # Wait 2 seconds
    page.wait_for_timeout(2000)

    # Get new value
    new_text = time_remaining.text_content()

    # They should be different (countdown should have progressed)
    assert initial_text != new_text


def test_reset_button(page: Page, page_url):
    """Test the reset/new timer button"""
    page.goto(page_url)

    # Start a timer
    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Verify timer screen is shown
    timer_screen = page.locator(".timer-screen.active")
    expect(timer_screen).to_be_visible()

    # Click reset button
    page.click("text=New Break Timer")

    # Setup screen should be visible again
    setup_screen = page.locator(".setup-screen.active")
    expect(setup_screen).to_be_visible()

    # Timer screen should not be visible
    timer_screen_after = page.locator(".timer-screen.active")
    expect(timer_screen_after).not_to_be_visible()


def test_invalid_time_alert(page: Page, page_url):
    """Test that starting without selecting a time shows alert"""
    page.goto(page_url)

    # Set up dialog handler
    dialog_message = []
    page.on("dialog", lambda dialog: (
        dialog_message.append(dialog.message),
        dialog.accept()
    ))

    # Try to start without selecting time
    page.click("text=Start Break Timer")

    # Should show alert
    page.wait_for_timeout(500)
    assert len(dialog_message) > 0
    assert "valid end time" in dialog_message[0].lower()


def test_current_times_update(page: Page, page_url):
    """Test that current UTC and CET times update when seconds are enabled"""
    page.goto(page_url)

    # Enable show seconds by clicking the visible toggle slider
    page.locator('label:has(#showSeconds) .toggle-slider').click()

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # UTC and CET are always shown
    utc_time = page.locator("#time-UTC")
    cet_time = page.locator("#time-Europe-Paris")

    # Get initial values
    initial_utc = utc_time.text_content()
    initial_cet = cet_time.text_content()

    # Wait 2 seconds
    page.wait_for_timeout(2000)

    # Get new values
    new_utc = utc_time.text_content()
    new_cet = cet_time.text_content()

    # Times should have updated (seconds changed)
    assert initial_utc != new_utc
    assert initial_cet != new_cet


def test_ui_elements_present(page: Page, page_url):
    """Test that all UI elements are present on setup screen"""
    page.goto(page_url)

    # Check quick buttons
    expect(page.locator("text=+15 Minutes")).to_be_visible()
    expect(page.locator("text=+30 Minutes")).to_be_visible()
    expect(page.locator("text=Next Full Hour")).to_be_visible()
    expect(page.locator("text=Next :15 After Hour")).to_be_visible()

    # Check inputs
    expect(page.locator("#customMinutes")).to_be_visible()
    expect(page.locator("#specificTime")).to_be_visible()

    # Check timezone selector
    expect(page.locator("#timezoneSelect")).to_be_visible()

    # Check toggle switches exist (checkboxes are hidden with opacity:0 for custom styling)
    expect(page.locator("#showSeconds")).to_be_attached()
    expect(page.locator("#playSound")).to_be_attached()

    # Check toggle labels are visible
    expect(page.locator("text=Show Seconds:")).to_be_visible()
    expect(page.locator("text=Play Sound at End:")).to_be_visible()

    # Check start button
    expect(page.locator("text=Start Break Timer")).to_be_visible()


def test_timezone_selector_present(page: Page, page_url):
    """Test that timezone selector is present and has options"""
    page.goto(page_url)

    timezone_select = page.locator("#timezoneSelect")
    expect(timezone_select).to_be_visible()

    # Check that it has multiple options
    options = timezone_select.locator("option")
    expect(options).to_have_count(14)  # Based on the timezones in the HTML


def test_default_timezones_displayed(page: Page, page_url):
    """Test that UTC and CET/CEST are always displayed"""
    page.goto(page_url)

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # UTC should be displayed
    utc_time = page.locator("#time-UTC")
    expect(utc_time).to_be_visible()

    # CET/CEST should be displayed
    cet_time = page.locator("#time-Europe-Paris")
    expect(cet_time).to_be_visible()


def test_additional_timezone_selection(page: Page, page_url):
    """Test selecting additional timezones"""
    page.goto(page_url)

    # Select Tokyo timezone using Ctrl+Click
    timezone_select = page.locator("#timezoneSelect")
    page.click("#timezoneSelect option[value='Asia/Tokyo']", modifiers=["Control"])

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Tokyo time should be displayed
    tokyo_time = page.locator("#time-Asia-Tokyo")
    expect(tokyo_time).to_be_visible()

    # Check ISO format (no seconds by default)
    iso_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
    expect(tokyo_time).to_have_text(re.compile(iso_pattern))


def test_multiple_timezone_selection(page: Page, page_url):
    """Test selecting multiple additional timezones"""
    page.goto(page_url)

    # Select multiple timezones
    timezone_select = page.locator("#timezoneSelect")
    page.click("#timezoneSelect option[value='America/New_York']", modifiers=["Control"])
    page.click("#timezoneSelect option[value='Asia/Tokyo']", modifiers=["Control"])
    page.click("#timezoneSelect option[value='Australia/Sydney']", modifiers=["Control"])

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # All selected timezones should be displayed
    expect(page.locator("#time-UTC")).to_be_visible()
    expect(page.locator("#time-Europe-Paris")).to_be_visible()
    expect(page.locator("#time-America-New_York")).to_be_visible()
    expect(page.locator("#time-Asia-Tokyo")).to_be_visible()
    expect(page.locator("#time-Australia-Sydney")).to_be_visible()


def test_timezone_times_update(page: Page, page_url):
    """Test that all timezone displays update when seconds are enabled"""
    page.goto(page_url)

    # Enable show seconds by clicking the visible toggle slider
    page.locator('label:has(#showSeconds) .toggle-slider').click()

    # Select an additional timezone
    page.click("#timezoneSelect option[value='Asia/Tokyo']", modifiers=["Control"])

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Get initial values
    utc_time = page.locator("#time-UTC")
    tokyo_time = page.locator("#time-Asia-Tokyo")

    initial_utc = utc_time.text_content()
    initial_tokyo = tokyo_time.text_content()

    # Wait 2 seconds
    page.wait_for_timeout(2000)

    # Get new values
    new_utc = utc_time.text_content()
    new_tokyo = tokyo_time.text_content()

    # Times should have updated (seconds changed)
    assert initial_utc != new_utc
    assert initial_tokyo != new_tokyo


def test_reset_clears_timezone_selection(page: Page, page_url):
    """Test that reset clears the timezone selection"""
    page.goto(page_url)

    # Select a timezone
    page.click("#timezoneSelect option[value='Asia/Tokyo']", modifiers=["Control"])

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Reset
    page.click("text=New Break Timer")

    # Timezone selection should be cleared
    timezone_select = page.locator("#timezoneSelect")
    selected_options = timezone_select.evaluate("el => Array.from(el.selectedOptions).length")
    assert selected_options == 0


def test_show_seconds_toggle_default(page: Page, page_url):
    """Test that show seconds toggle is disabled by default"""
    page.goto(page_url)

    # Check that toggle is not checked (use force because checkbox is hidden with opacity:0)
    show_seconds_toggle = page.locator("#showSeconds")
    expect(show_seconds_toggle).not_to_be_checked()


def test_show_seconds_enabled(page: Page, page_url):
    """Test that enabling show seconds displays time with seconds"""
    page.goto(page_url)

    # Enable show seconds by clicking the visible toggle slider
    page.locator('label:has(#showSeconds) .toggle-slider').click()

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Wait a moment for times to update
    page.wait_for_timeout(1000)

    # Check end time format (should have seconds)
    end_time = page.locator("#endTimeDisplay")
    iso_pattern_with_seconds = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    expect(end_time).to_have_text(re.compile(iso_pattern_with_seconds))

    # Check UTC time format (should have seconds)
    utc_time = page.locator("#time-UTC")
    expect(utc_time).to_have_text(re.compile(iso_pattern_with_seconds))

    # Check CET/CEST time format (should have seconds)
    cet_time = page.locator("#time-Europe-Paris")
    expect(cet_time).to_have_text(re.compile(iso_pattern_with_seconds))


def test_play_sound_toggle_default(page: Page, page_url):
    """Test that play sound toggle is disabled by default"""
    page.goto(page_url)

    # Check that toggle is not checked (checkbox is hidden with opacity:0)
    play_sound_toggle = page.locator("#playSound")
    expect(play_sound_toggle).not_to_be_checked()


def test_play_sound_toggle_exists(page: Page, page_url):
    """Test that play sound toggle can be enabled"""
    page.goto(page_url)

    # Enable play sound by clicking the visible toggle slider
    page.locator('label:has(#playSound) .toggle-slider').click()

    # Verify checkbox is now checked
    play_sound_toggle = page.locator("#playSound")
    expect(play_sound_toggle).to_be_checked()


def test_reset_clears_toggles(page: Page, page_url):
    """Test that reset clears both toggle switches"""
    page.goto(page_url)

    # Enable both toggles by clicking the visible toggle sliders
    page.locator('label:has(#showSeconds) .toggle-slider').click()
    page.locator('label:has(#playSound) .toggle-slider').click()

    page.click("text=+15 Minutes")
    page.click("text=Start Break Timer")

    # Reset
    page.click("text=New Break Timer")

    # Both toggles should be unchecked
    expect(page.locator("#showSeconds")).not_to_be_checked()
    expect(page.locator("#playSound")).not_to_be_checked()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
