$(document).ready(function() {
    $.each(langs, function(idx, lang_code){
        var id_title = '#id_title_' + lang_code;
        var id_slug = '#id_slug_' + lang_code;
        $(id_title).on('focus', function() {
            $(id_slug).data('previous-val', $(id_slug).val());
            $(this).data('previous-val', $(this).val());
        });

        $(id_title).on('keyup keydown keypress blur', function() {
            if ($('body').hasClass('create') || !$(id_slug).data('previous-val').length || cleanForSlug($(id_title).data('previous-val')) === $(id_slug).data('previous-val')) {
                // only update slug if the page is being created from scratch, if slug is completely blank, or if title and slug prior to typing were identical
                $(id_slug).val(cleanForSlug($(id_title).val()));
            }
        });
    });
});
