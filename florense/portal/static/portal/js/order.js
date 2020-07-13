//Enable the name on browse file
function enableNamePathOnInput(){
    $('.custom-file-input').on('change',function(){
                    var fileName = $(this).val();
                    $(this).next('.custom-file-label').html(fileName);
    })
}


//$('.carousel').carousel('pause');

function addRoom(room, labelsList, productsList){
    $(".carousel-item").removeClass('active');
    $(".carousel-indicators").children().removeClass('active');

    var labels = getHtmlLabels(room, labelsList);
    var products = getHtmlProducts(room, productsList);

    $(`<div class="carousel-item active">
            <h5 class="orders subtitle text-center">${room}</h5>
            <input type="hidden" name="room" value="${room}">
            <div id="${room}-label" class="flex flex-start flex-wrap">
            ${labels}
            </div>
            <section id="${room}-product" class="container flex row flex-start">
            ${products}
            </section>
        </div>`).appendTo('.carousel-inner');

    $('<li data-target="#carouselRoom" class="active" data-slide-to="'+$(".carousel-indicators").children().length+'"></li>').appendTo('.carousel-indicators')
    $('.item').first().addClass('active');
    enableNamePathOnInput();
}

function getHtmlLabels(room, labels){
    var labelsHtml = '';

    for(var item in labels) {
        labelsHtml += `<div class="label-item">
                        <label>${labels[item]}</label>
                        <input name="label-${room}-${labels[item]}" type="text" class="form-control">
                      </div>`
    }
    return labelsHtml;
}

function getHtmlProducts(room, products){
    var productsHtml = '';

    for(var item in products) {
        productsHtml += `<div class="item product-item">
                        <p>${products[item]}
                            <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-file-earmark-check"
                                 fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9 1H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h5v-1H4a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h5v2.5A1.5 1.5 0 0 0 10.5 6H13v2h1V6L9 1z"/>
                                <path fill-rule="evenodd"
                                      d="M15.854 10.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708l1.146 1.147 2.646-2.647a.5.5 0 0 1 .708 0z"/>
                            </svg>
                            <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle" fill="currentColor"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd"
                                      d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                <path fill-rule="evenodd"
                                      d="M11.854 4.146a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708-.708l7-7a.5.5 0 0 1 .708 0z"/>
                                <path fill-rule="evenodd"
                                      d="M4.146 4.146a.5.5 0 0 0 0 .708l7 7a.5.5 0 0 0 .708-.708l-7-7a.5.5 0 0 0-.708 0z"/>
                            </svg>
                        </p>
                        <div class="custom-file">
                            <input name="product-${room}-${products[item]}" type="file" class="custom-file-input" id="customFile">
                            <label class="custom-file-label" for="customFile">Escolher arquivo</label>
                        </div>
                    </div>`
    }
    return productsHtml;
}







