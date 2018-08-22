$(document).ready(function (){
    //original field values
    var field_values = {
            //id        :  value
            'username'  : 'username',
            'password'  : 'password',
            'cpassword' : 'password',
            'firstname'  : 'first name',
            'lastname'  : 'last name',
            'email'  : 'email address'
    };


    //inputfocus
    // $('input#username').inputfocus({ value: field_values['username'] });
    // $('input#password').inputfocus({ value: field_values['password'] });
    // $('input#cpassword').inputfocus({ value: field_values['cpassword'] });
    // $('input#lastname').inputfocus({ value: field_values['lastname'] });
    // $('input#firstname').inputfocus({ value: field_values['firstname'] });
    // $('input#email').inputfocus({ value: field_values['email'] });



    //reset progress bar
    $('#progress').css('width','0');
    $('#progress_text').html('0% Complete');
    //first_step
    $('form').submit(function(){ return false; });
    $('#submit_first').click(function(){
        // console.log($('.disk_table').selectpicker('val'));


        //remove classes
        $('#first_step input').removeClass('error').removeClass('valid');

        //ckeck if inputs aren't empty
        var fields = $('#first_step input[type=text], #first_step input[type=password]');
        var error = 0;
        fields.each(function(){
            var value = $(this).val();
            if( value.length<4 || value==field_values[$(this).attr('id')] ) {
                $(this).addClass('error');
                $(this).effect("shake", { times:3 }, 50);
                
                error++;
            } else {
                $(this).addClass('valid');
            }
        });        

        if(!error) {
            if( $('#password').val() != $('#cpassword').val() ) {
                    $('#first_step input[type=password]').each(function(){
                        $(this).removeClass('valid').addClass('error');
                        $(this).effect("shake", { times:3 }, 50);
                    });
                    
                    return false;
            } else {   
                //update progress bar
                $('#progress_text').html('33% Complete');
                $('#progress').css('width','113px');
                
                //slide steps
                $('#first_step').slideUp();
                $('#second_step').slideDown();     
            }               
        } else return false;
    });

    $("#submit_second_pre").click(function () {
        $('#second_step').slideUp();
        $('#first_step').slideDown();

    });
    $('#submit_second').click(function(){
        var disk_type = $("#disk_type option:selected").val();
        var route = $("#route").val();
        var share_name = $("#share_name").val();
        console.log(share_name);
        console.log(route);
        console.log(disk_type);
        var disk_name = $("#disk_name").val();
        console.log(disk_name);
        $("#disk_type_change").text(disk_type);
        $("#share_name_change").text(share_name);
        //remove classes
        $('#second_step input').removeClass('error').removeClass('valid');

        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;  
        var fields = $('#second_step input[type=text]');
        var error = 0;
        fields.each(function(){
            var value = $(this).val();
            if( value.length<1 || value==field_values[$(this).attr('id')] || ( $(this).attr('id')=='email' && !emailPattern.test(value) ) ) {
                $(this).addClass('error');
                $(this).effect("shake", { times:3 }, 50);
                
                error++;
            } else {
                $(this).addClass('valid');
            }
        });

        if(!error) {
                //update progress bar
                $('#progress_text').html('66% Complete');
                $('#progress').css('width','226px');
                
                //slide steps
                $('#second_step').slideUp();
                $('#third_step').slideDown();     
        } else return false;

    });

    $("#submit_third_pre").click(function () {
        $('#third_step').slideUp();
        $('#second_step').slideDown();

    });
    $('#submit_third').click(function(){
        var cold_time = $("#cold_time option").val();
        console.log(cold_time);
        //update progress bar
        $('#progress_text').html('100% Complete');
        $('#progress').css('width','339px');

        //prepare the fourth step
        var fields = [$('#username').val(),
            $('#password').val(),
            $('#email').val(),
            $('#firstname').val() + ' ' + $('#lastname').val(),
            $('#age').val(),
            $('#gender').val(),
            $('#country').val()];
        var tr = $('#fourth_step tr');
        tr.each(function(){
            //alert( fields[$(this).index()] )
            $(this).children('td:nth-child(2)').html(fields[$(this).index()]);
        });
                
        //slide steps
        $('#third_step').slideUp();
        $('#fourth_step').slideDown();            
    });

    $("#submit_fourth_pre").click(function () {
        $('#fourth_step').slideUp();
        $('#third_step').slideDown();

    });
    $('#submit_fourth').click(function(){
        //send information to server
        alert('Data sent');
    });

});