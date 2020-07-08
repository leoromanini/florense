//Enable the name on browse file
$('.custom-file-input').on('change',function(){
                var fileName = $(this).val();
                $(this).next('.custom-file-label').html(fileName);
})

//$('.carousel').carousel('pause');

function addRoom(room){
    $(".carousel-item").removeClass('active');
    $(".carousel-indicators").children().removeClass('active');

    $(`<div class="carousel-item active">
            <h5 class="orders subtitle text-center">${room}</h5>
            <div id="${room}-label" class="flex space-between flex-wrap">
            </div>
            <section id="${room}-product" class="container flex row space-between">
            </section>
        </div>`).appendTo('.carousel-inner');

    $('<li data-target="#carouselRoom" class="active" data-slide-to="'+$(".carousel-indicators").children().length+'"></li>').appendTo('.carousel-indicators')
    $('.item').first().addClass('active');
}