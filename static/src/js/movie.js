var movies;

function get_movie_list(el) {
    $('div.myspinner').css("display", "block");
    var moviename = $('input.searchinput')[0].value;
    $.ajax({
        url: '/getmovies',
        type: "POST",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'movie': moviename}}),
        success: function(data){
            $('div.myspinner').css("display", "none");
            movies = data.result.data
            var ul_el = document.getElementById("movielist");
            ul_el.innerHTML = "";
            $('div.movielistdiv').css('display', 'block');
            movies.forEach(function(movie) {
                var el_li = document.createElement('li');
                el_li.classList.add('list-group-item');
                el_li.classList.add('movie');
                el_li.setAttribute('id', movie.id);
                el_li.appendChild(document.createTextNode(movie.name_russian + " (" + movie.year + " год, " + movie.country_ru + ")"));
                ul_el.appendChild(el_li);
            });
        }
    });
}

$(document).on('click', 'li.movie', function (el) {
    let curmovie = movies.find(m => m.id === parseInt(el.target.id));
    $.ajax({
        url: '/getimg',
        type: "POST",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'src': curmovie.small_poster}}),
        success: function(data){
            $("textarea[name='fieldtoupload']").val(data.result);
            $("textarea[name='fieldtoupload']").change();
        }
    });
    $("input[name='name']").val(curmovie.name_russian);
    $("input[name='name']").change();
    $("input[name='year']").val(curmovie.year);
    $("input[name='year']").change();
    $("input[name='country']").val(curmovie.country_ru);
    $("input[name='country']").change();
    $("input[name='rating_kp']").val(curmovie.rating_kp);
    $("input[name='rating_kp']").change();
    $("input[name='rating_imdb']").val(curmovie.rating_imdb);
    $("input[name='rating_imdb']").change();
    $('#select_movie').css("display", "none");
});
