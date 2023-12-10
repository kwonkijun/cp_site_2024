var isLoading = false;
var nextPage = 1; // 시작은 항상 두 번째 페이지부터 데이터를 불러옴
var total_pages = 9999;

// URL에서 keyword 파라미터의 값을 가져옵니다.
var urlParams = new URLSearchParams(window.location.search);
var keyword = urlParams.get('keyword');

function loadMoreProducts() {
    if (isLoading || nextPage > total_pages) {
        return; // 이미 로딩 중이거나 더 이상 로드할 페이지가 없을 경우 함수 종료
    }
    isLoading = true;

    // AJAX 요청을 통해 다음 페이지의 데이터를 불러옵니다.
    $.ajax({
        url: '/dynamic',
        type: 'GET',
        dataType: 'json', // 서버로부터 JSON 형식의 응답을 기대합니다.
        data: {
            page: nextPage,
            keyword: keyword
        },
        success: function (response) {
            var newProductHtml = '';
            response.product_data.forEach(function (product) {
                newProductHtml += '<div class="col-md-4 col-xs-6">' +
                    '<div class="product">' +
                    '<div class="product-img">' +
                    '<img src="../static/img/' + product.image_path + '" alt="">' +
                    '<div class="product-label">';
                if (product.discount_label) {
                    newProductHtml += '<span class="sale">-' + product.discount_label + '%</span>';
                }
                if (product.new_label === 'N') {
                    newProductHtml += '<span class="new">HOT</span>';
                }
                newProductHtml += '</div></div>' +
                    '<div class="product-body">' +
                    '<p class="product-category">' + product.category + '</p>' +
                    '<h3 class="product-name"><a href="#product' + product.product_id + '_detail.html">' + product.name + '</a></h3>' +
                    '<h4 class="product-price">' + product.price.toLocaleString() + '원';
                if (product.original_price) {
                    newProductHtml += '<del class="product-old-price">' + product.original_price.toLocaleString() + '</del>';
                }
                newProductHtml += '</h4>' +
                    '<div class="product-rating sub_cnt">';
                for (var star = 1; star <= 5; star++) {
                    if (star <= product.rating) {
                        newProductHtml += '<i class="fa fa-star"></i>';
                    } else if (star - 1 < product.rating) {
                        newProductHtml += '<i class="fa fa-star-half-o"></i>';
                    } else {
                        newProductHtml += '<i class="fa fa-star-o"></i>';
                    }
                }
                newProductHtml += ' (' + product.rating_count + ') ' +
                    '</div>' +
                    '<div class="product-btns">' +
                    '<button class="add-to-wishlist"><i class="fa fa-heart-o"></i><span class="tooltipp">add to wishlist</span></button>' +
                    '<button class="quick-view"><i class="fa fa-eye"></i><span class="tooltipp">quick view</span></button>' +
                    '</div></div>' +
                    '<div class="add-to-cart">' +
                    '<button class="add-to-cart-btn"><i class="fa fa-shopping-cart"></i> add to cart</button>' +
                    '</div></div></div>';
            });

            $('#product-container').append(newProductHtml);
            nextPage++; // 다음 페이지 번호 증가
            isLoading = false;
            total_pages = response.total_pages
        },
        error: function (xhr, status, error) {
            console.error("An error occurred while loading more pruducts: ", status, error);
            isLoading = false;
        }
    });
}
loadMoreProducts();
// 스크롤 이벤트 리스너를 추가하여 페이지 끝에 도달했을 때 loadMoreProducts 함수를 호출합니다.
$(window).scroll(function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 300) { // 페이지 하단에서 800px 이내로 스크롤되면
        loadMoreProducts(); // 추가 포스트를 로드
    }
});