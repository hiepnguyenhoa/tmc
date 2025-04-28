document.addEventListener("DOMContentLoaded", function () {
    // Get the teacher dropdown, title input, and slug input fields
    const teacherDropdown = document.querySelector("#id_teacher");
    const titleInput = document.querySelector("#id_title");
    const slugInput = document.querySelector("#id_slug");

    if (teacherDropdown && titleInput && slugInput) {
        // Listen for changes to the teacher dropdown
        teacherDropdown.addEventListener("change", function () {
            // Get the selected teacher's name
            const selectedOption = teacherDropdown.options[teacherDropdown.selectedIndex];
            const teacherName = selectedOption.text;

            // Update the title field with the teacher's name
            titleInput.value = teacherName;

            // Generate a slug from the teacher's name
            const slug = teacherName
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, "-") // Replace non-alphanumeric characters with hyphens
                .replace(/^-+|-+$/g, ""); // Remove leading/trailing hyphens

            // Set the slug input field value
            slugInput.value = slug;
        });
    }
});