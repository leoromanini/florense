//Enable the name on browse file
function enableNamePathOnInput(){
    $('.custom-file-input').on('change',function(){
                    var fileName = $(this).val();
                    $(this).next('.custom-file-label').html(fileName);
    })
}

function addRoom(roomName, roomId, labelsListName, labelListId,
                    productsListName, productListId, labelsContentList=undefined,
                    productAllocationIdList=undefined, productAllocationByProductIdList=undefined,
                    productAllocationIsActiveList=undefined, elementButton=undefined){

    $(".carousel-item").removeClass('active');
    $(".carousel-indicators").children().removeClass('active');

    var labels = getHtmlLabels(roomId, labelsListName, labelListId, labelsContentList);
    var products = getHtmlProducts(roomId, productsListName, productListId,
                                    productAllocationIdList, productAllocationByProductIdList, productAllocationIsActiveList);

    $(`<div class="carousel-item active ${roomId}-item">
            <h5 class="orders subtitle text-center">${roomName}</h5>
            <input type="hidden" name="room" value="${roomId}">
            <div id="${roomId}-label" class="flex flex-start flex-wrap">
            ${labels}
            </div>
            <section id="${roomId}-product" class="container flex row flex-start">
            ${products}
            </section>
        </div>`).appendTo('.carousel-inner');

    $(`<li data-target="#carouselRoom" class="active ${roomId}-indicator carousel-indicator" data-slide-to="`+$(".carousel-indicators").children().length+'"></li>').appendTo('.carousel-indicators')
    $('.item').first().addClass('active');
    enableNamePathOnInput();

    addElementOnConsultButton(roomName, roomId);

    $(`#option-new-${roomId}`).remove();
}

function addElementOnConsultButton(roomName, roomId){
    $(`<a class="dropdown-item pointer" onclick="goToItemOnCarousel('${roomId}')">${roomName}</a>`).appendTo('#consultButton');
}

function goToItemOnCarousel(roomId){
    $(".carousel-item").removeClass('active');
    $(".carousel-indicator").removeClass('active');
    $(`.${roomId}-indicator`).addClass('active');
    $(`.${roomId}-item`).addClass('active');

}

function getHtmlLabels(roomId, labelsName, labelsId, labelsContentList=undefined){
    var labelsHtml = '';

    for(var item in labelsName) {

        labelsHtml += `<div class="label-item">
                        <label>${labelsName[item]}</label>
                        <input name="label-${roomId}-${labelsId[item]}" type="text" class="form-control"
                            value="${labelsContentList?.[item]}">
                      </div>`
    }
    return labelsHtml;
}

function getHtmlProducts(roomId, productsName, productsId, productAllocationIdList=undefined,
                            productAllocationByProductIdList=undefined, productAllocationIsActiveList=undefined){
    var productsHtml = '';

    for(const [index, item] of productsId.entries()) {

        productsHtml += `<div class="item product-item">
                        <p>${productsName[index]} `

        if (productAllocationIdList != undefined && productAllocationByProductIdList.includes(item)){
            indexOfProductAllocated = productAllocationByProductIdList.indexOf(item);
            productsHtml += `<svg onclick="downloadProductImage(${productAllocationIdList[indexOfProductAllocated]})" width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-cloud-download-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path fill-rule="evenodd" d="M8 0a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 4.095 0 5.555 0 7.318 0 9.366 1.708 11 3.781 11H7.5V5.5a.5.5 0 0 1 1 0V11h4.188C14.502 11 16 9.57 16 7.773c0-1.636-1.242-2.969-2.834-3.194C12.923 1.999 10.69 0 8 0zm-.354 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V11h-1v3.293l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z"/>
                            </svg> `
        }

        if (profile == 'inspector'){
            productsHtml += `<a href="#" class="badge badge-secondary">APROVAR</a>`
        }

        productsHtml += `</p><div class="custom-file">
                            <input name="product-${roomId}-${item}" type="file" class="custom-file-input" id="customFile">
                            <label class="custom-file-label" for="customFile">Escolher arquivo</label>
                        </div>
                    </div>`
    }
    return productsHtml;
}

function downloadProductImage(allocationId){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/download-product-image', true);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function () {
        if (this.status === 200) {
            var filename = "";
            var disposition = xhr.getResponseHeader('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
            }
            var type = xhr.getResponseHeader('Content-Type');

            var blob;
            if (typeof File === 'function') {
                try {
                    blob = new File([this.response], filename, { type: type });
                } catch (e) { /* Edge */ }
            }
            if (typeof blob === 'undefined') {
                blob = new Blob([this.response], { type: type });
            }

            if (typeof window.navigator.msSaveBlob !== 'undefined') {
                // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                window.navigator.msSaveBlob(blob, filename);
            } else {
                var URL = window.URL || window.webkitURL;
                var downloadUrl = URL.createObjectURL(blob);

                if (filename) {
                    // use HTML5 a[download] attribute to specify filename
                    var a = document.createElement("a");
                    // safari doesn't support this yet
                    if (typeof a.download === 'undefined') {
                        window.location.href = downloadUrl;
                    } else {
                        a.href = downloadUrl;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                    }
                } else {
                    window.location.href = downloadUrl;
                }

                setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
            }
        }
    };
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));

    xhr.send(JSON.stringify({'allocationId': allocationId}));
};






