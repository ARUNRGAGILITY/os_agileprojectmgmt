(function($) {
    $(document).ready(function() {
        // When the project is changed, update the project_role field
        $('#id_project').change(function() {
            var project_id = $(this).val();
            var projectRoleField = $('#id_project_role');
            projectRoleField.html('');  // Clear previous options

            if (project_id) {
                // Fetch the related project roles via AJAX
                $.ajax({
                    url: '/admin/get_project_roles/',  // Update with the correct URL
                    data: {
                        'project_id': project_id
                    },
                    success: function(data) {
                        projectRoleField.html(data);
                    }
                });
            }
        });
    });
})(django.jQuery);
