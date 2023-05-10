var selectedOption;
var dict;
var checked_val = {};

$(document).ready(function(){
    $('#sym').change(function(){
        selectedOption = $(this).val();
        $('#days').prop('disabled', false);
        //alert(selectedOption)
    });


    $('#next_button3').click(function(){
        var days = $(this).val();
        var dis = selectedOption
        if(dis == null){
            alert("please select symptom")
        }
        else{
            //alert(dis+''+days)
            $.ajax({
                type: 'GET',
                url: 'check_sym',
                data: {'days': days, 'dis':dis},
                success: function(response){
                        var days = days;
                        var dis = dis;
                        dict = response.result;
                        //alert(dict);
                        $('#symptoms-list').empty();
                        for(var key in response.result){
                            $('#symptoms-list').append('<label class="radio-sym">'+response.result[key]+'</label><label class="radio-sym"><input type="radio" name="'+response.result[key]+'" value="yes">Yes</label><label class="radio-sym"><input type="radio" name="'+response.result[key]+'" value="no">No</label><br><br>');
                            //dict[response.result[key]] = $('input[name="'+response.result[key]+'"]:checked').val();
                            //alert($('input[name="'+response.result[key]+'"]:checked').val())
                        }
                        //console.log(dict)
                        //$('#symptoms1').append('<button name ="submit" type="submit" value="submit" id="submit">Submit</button> ');
                }
            });
        }
    });

    $(document).ready(function(){
        $('#submit_button').click(function(){
            var days = $('#days').val();
            var dis = $('#sym').val();
            var list = new Array();
            //var l1 = new Array();
            let l='';
            for(var key in dict){
                //checked_val[dict[key]]=$('input[name="'+dict[key]+'"]:checked').val();
                //list.push($('input[name="'+dict[key]+'"]:checked').val());

                if($('input[name="'+dict[key]+'"]:checked').val()=='yes')
                    list.push(dict[key]);
                //alert($('input[name="'+dict[key]+'"]:checked').val());
            }

            //console.log(list)

            for(var i=0;i<list.length;i++){
            
                    l+=list[i]+' '
            }
            l=l.trim();
            //console.log(days);
            //console.log(dis);
            //console.log(checked_val);
            //console.log(l);
            $.ajax({
                type: 'GET',
                url: 'check_disease',
                //async: true,
                data: {'days': days, 'dis':dis, 'list': l},
                success: function(response){
                    $('#result').append("You may have: "+response.present+"<br/>"+ response.desc1);
                    console.log("res "+response.sec);
                    //alert('success');
    
                }
            });
    
    
        });
    
    });

});