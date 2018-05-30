$(document).ready(function(){

  var settings = {
    "url": "http://127.0.0.1:5001/getDocuments",
    "method": "GET",
    "cache":false
  }

  $.ajax(settings).done(function (response) {
    // alert('Response recieved AJAX. ');
    var i = 0;
    var length = response.length;
    for (var key in response) {
      if (response.hasOwnProperty(key)) {
          $('#resultstable tbody').append('<tr id="'+response[key]+'"><th scope="row">'+response[key]+'</th></tr>');
          // $("#resultstable").load("#resultstable");
          $('#displayresults').show();
      }
    }
  });
});

$(document).on("click", "#resultstable tr", function(e) {

  var filename = this.id
  // alert(this.id);


  var file_path = "static/CorpusFilesWithFeatures/"+filename.split(".")[0]+"_outputTask3.txt"

  $('#file_contents').attr("src", file_path);

  $('#list').show();
  $('#displayresults').hide();

  // var settings = {
  //   "async": true,
  //   "crossDomain": true,
  //   "url": "http://127.0.0.1:5000/getFeatures?filename="+this.id,
  //   "method": "GET",
  //   "headers": {
  //     "cache-control": "no-cache",
  //     "postman-token": "8bd081e8-379a-d3f4-9cde-59af957967db"
  //   }
  // }
  //
  // $.ajax(settings).done(function (response) {
  //
  //   // response = response("\n","<br>");
  //   alert(response);
  //   console.log("response: ",JSON.stringify(response, null, 2));
  //
  //   var file_path = "static/Task3Output/"+filename.split(".")[0]+"_outputTask3.txt"
  //
  //   // var src_path = "{{ url_for('static', filename='"+ file_path +"') }}"
  //
  //   //alert(src_path)
  //
  //   $('#file_contents').attr("src", file_path);
  //
  //   $('#list').show();
  //   $('#displayresults').hide();
  //
  //
  //
  //   //
  //   // url = 'http://127.0.0.1:5000/task3.html?name=' + encodeURIComponent();
  //   // document.location.href = url;
  //
  //   $('#question').html("Features of document: ");
  //   $('#answer').load("/Users/pranav.bhatiaibm.com/Dropbox/Ebooks/NLP/Project/webpage/app/Task3Output/Q1_outputTask3.txt");
  //   $('#myModal').modal('show');
  // });
});
