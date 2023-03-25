$(document).ready(function(){
    $("#submit").on('',function(e) {
        var data = new FormData($("#predictor-form")[0]);

        $.ajax({
            type: 'POST',
            url: 'predict',
            data: data,
            processData: false,
            contentType: false,
            success: function(r) {
            $('#output').html(
            `<div class="col-lg-5" style="padding-top:30px">
                  <span class="border border-primary">
                    <img src="{{ r.user_image }}" alt="User Image" class="img-thumbnail" style="width:250px;height:250px;float:right">
                  </span>
                </div>
                <div class="col-lg-5" style="padding-top:30px">
                  <h4>Fruit name is <mark style="background-color:#04aa6d;color:white;border-radius:5px">{{r.fruit}}</mark></h4>
                  <h4>Probabilities : {{r.prob}}</h4>
                </div>
            `);
            },
            error: function(r) {
              console.log('error', r);
            }
        });
    })
});
