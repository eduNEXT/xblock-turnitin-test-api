/* Javascript for TurnitinXBlock. */
function TurnitinXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    function showEULA(htmlContent) {
        $('#eulaModal .modal-content p').html(htmlContent); // Establece el contenido HTML en el párrafo del modal
        $('#eulaModal').show();
    }

    function closeModal() {
        $('#eulaModal', element).hide();
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $('#viewEULA', element).click(function() {
        var handlerUrl = runtime.handlerUrl(element, 'get_eula_agreement'); // Asumo que el nombre de la acción es 'fetch_eula_content'
    
        $.ajax({
            type: "POST", // Asumo que estamos obteniendo el contenido, así que usamos GET en lugar de POST
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: function(response) {
                showEULA(response); // Usa la respuesta como contenido HTML del modal
            },
            error: function() {
                //alert('Error al obtener el contenido del EULA.');
            }
        });
    });

    function updateSelectedFileName() {
        var fileName = $(this).val().split('\\').pop();
        var fileExtension = fileName.split('.').pop().toLowerCase();
    
        if (fileExtension === 'doc' || fileExtension === 'docx') {
            if (fileName) {
                $(this).siblings('.selected-filename').text(fileName);
                $(this).siblings('label').addClass('file-selected').text('Cambiar archivo'); // Cambiar texto a "Cambiar archivo"
            } else {
                $(this).siblings('.selected-filename').text('Ningún archivo seleccionado');
                $(this).siblings('label').removeClass('file-selected').text('Elegir archivo'); // Revertir texto a "Elegir archivo"
            }
        } else {
            alert('Por favor, selecciona un archivo .doc o .docx');
            $(this).val('');
            $(this).siblings('.selected-filename').text('Ningún archivo seleccionado');
            $(this).siblings('label').removeClass('file-selected').text('Elegir archivo'); // Revertir texto a "Elegir archivo"
        }
    }
    $('#file', element).on('change', updateSelectedFileName);
    $('.modal-content button').click(closeModal);


    $(function ($) {
        /*
        Use `gettext` provided by django-statici18n for static translations

        var gettext = TurnitinXBlocki18n.gettext;
        */

        /* Here's where you'd do things on page load. */
    });
}
