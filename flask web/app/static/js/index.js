$(document).ready(function(){

  $("#searchresults").click(function() {
      $('#displayresults').show();
      // alert($("#query").val());
      var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://127.0.0.1:5000/getResults?query="+$("#query").val(),
        "method": "GET",
        "headers": {
          "cache-control": "no-cache",
          "postman-token": "8bd081e8-379a-d3f4-9cde-59af957967db"
        }
      }

      $.ajax(settings).done(function (response) {
        for (var key in response) {
          if (response.hasOwnProperty(key)) {
              $('#resultstable tbody').append('<tr id="'+response[key]+'"><th scope="row">'+key+'</th><td>'+response[key]+'</td></tr>');
          }
        }
      });

  });
});

$(document).on("click", "#resultstable tr", function(e) {
  // alert(this.id);

  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "http://127.0.0.1:5000/getText?filename="+this.id,
    "method": "GET",
    "headers": {
      "cache-control": "no-cache",
      "postman-token": "8bd081e8-379a-d3f4-9cde-59af957967db"
    }
  }

  $.ajax(settings).done(function (response) {

    response = response.replace("\n"," ");
    var questionpattern = /(.)*\?/g;
    var answerpattern = /\?(.)*/g;


    question = response.match(questionpattern)
    answer = response.match(answerpattern)
    answer = response.replace(question,"")
    // alert(question);
    // alert(answer);
    $('#question').html(question);
    $('#answer').html(answer);
    $('#myModal').modal('show');
  });




});
