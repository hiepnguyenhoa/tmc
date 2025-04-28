document.addEventListener("DOMContentLoaded", function () {
    // Get the teacher dropdown and title input fields
    const teacherDropdown = document.querySelector("#id_teacher");
    const titleInput = document.querySelector("#id_title");

    if (teacherDropdown && titleInput) {
        // Listen for changes to the teacher dropdown
        teacherDropdown.addEventListener("change", function () {
            // Get the selected teacher's name
            const selectedOption = teacherDropdown.options[teacherDropdown.selectedIndex];
            const teacherName = selectedOption.text;

            // Update the title field with the teacher's name
            titleInput.value = teacherName;

            // Trigger a change event on the title field to ensure Wagtail detects the update
            titleInput.dispatchEvent(new Event("change"));
        });
    }
});