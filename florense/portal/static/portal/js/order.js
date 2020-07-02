$('.custom-file-input').on('change',function(){
                var fileName = $(this).val();
                $(this).next('.custom-file-label').html(fileName);
})

$('.carousel').carousel('pause');