document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        console.log("Script loaded after delay"); // Debug statement

        // Get the teacher dropdown and title input fields
        const teacherDropdown = document.querySelector("#id_teacher");
        const titleInput = document.querySelector("#id_title");

        if (teacherDropdown && titleInput) {
            console.log("Teacher dropdown and title input found"); // Debug statement

            // Listen for changes to the teacher dropdown
            teacherDropdown.addEventListener("change", function () {
                console.log("Teacher dropdown changed"); // Debug statement

                // Ensure the dropdown has options
                if (teacherDropdown.options.length > 0) {
                    const selectedOption = teacherDropdown.options[teacherDropdown.selectedIndex];
                    const teacherName = selectedOption.text;

                    console.log("Selected teacher name:", teacherName); // Debug statement

                    // Update the title field with the teacher's name
                    titleInput.value = teacherName;

                    // Trigger a change event on the title field to ensure Wagtail detects the update
                    titleInput.dispatchEvent(new Event("change"));
                } else {
                    console.error("No options available in the teacher dropdown");
                }
            });
        } else {
            console.error("Teacher dropdown or title input not found"); // Debug statement
        }
    }, 500); // Add a 500ms delay
});