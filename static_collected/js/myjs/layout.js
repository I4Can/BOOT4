function about (){
            $('.about').click(function(){
                location.href='/about#pagerModal';
            })
        }

       function manage (){
            if("{{request.session.user_id|safe}}"=="1"){
                $('#manage').click(function(){
                    location.href='/backend/';
                })
            }
       }
       function cLike(status){
            $('.fa-thumbs-up').click(function(){
                if(status){
                    $(this).toggleClass('text-info');
                    $.ajax({
                    headers: {"X-CSRFToken":$.cookie("csrftoken")},
                    url:'/like/',
                    type:'POST',
                    dataType'json',
                    data:{'article_id':$(this).parent().attr('id'),'path':$('#path').val()},
                    success:function(arg){
                        $(this).text(arg.like);
                    }
                    })
                }
                else{
                    alert(13);
                    $('#makeLogin').modal('show');
                }
            })
       }

       function status(){
            var status="{{request.session.username|safe}}"
            if(status){
                $('.fa-power-off').addClass('fa-user');
                $('.fa-power-off').addClass('text-dark');
                $('.fa-power-off').removeClass('fa-power-off');
                $('#changeStatus').click(function(){
                $.ajax({
                    headers: {"X-CSRFToken":$.cookie("csrftoken")},
                    url:'/status/',
                    type:'POST',
                    success:function(){
                        location.reload();
                    }
                })
                })
            }
            else{
                $('.fa-power-off').attr('data-target','#makeLogin');
                $('.fa-power-off').click(function(){
            })
       }

            $('.fa-power-off,.fa-user').hover(function(){
                $(this).toggleClass('text-dark');
            },
            function(){
                $(this).toggleClass('text-dark');
            })
            msgCheckStatus(status);
            cLike(status);
       }

        function msgCheckStatus(status){
            $('.sendReply').click(function(){
            if(status){
                return true;
            }
            else{
                $('#makeLogin').modal('show');
                return false;
            }
            })
        }

        function infoSubmit(){
        $('#subButton').click(function(){
            if($('#inputNickname').val()){
                var form = new FormData();
                avatar=$('#avatar-select')[0].files[0];
                form.append('nickname',$('#inputNickname').val());
                form.append('gender',$('#inputGender').val());
                form.append('presentation',$('#inputPresentation').val());
                form.append('avatar',avatar);
                $.ajax({
                headers: {"X-CSRFToken":$.cookie("csrftoken")},
                url:'/edit_info/',
                type:'POST',
                data: form,
                dataType:'json',
                processData: false,
                contentType: false,
                success:function(arg){
                    if(arg.status){
                        alert(arg.msg);
                        location.reload();
                    }
                    else{
                        alert(arg.msg);
                    }
                }
            })
            }
            }
        )
    }

    function renderInfo(){
        $('#inputGender').children().each(function(){
            if($(this).val()==$('#gender').val()){
                    $(this).attr('selected','selected');
                }
        })
        $('#avatar-select').change(function(){
            var file = document.getElementById("avatar-select").files[0];
            var reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload=function(e){
                var img=$("#user-avatar");
                img.attr('src',this.result);
            }

        })

        }

        function signSubmit(){
        $('#signButton').click(function(){
            if($('#inputUsername').val()&&$('#inputPassword').val()){
                $.ajax({
                headers: {"X-CSRFToken":$.cookie("csrftoken")},
                url:'/sign/',
                type:'POST',
                data:$('.form-signin').serialize(),
                dataType:'json',
                success:function(arg){
                    if(arg.status){
                        alert(arg.msg);
                        location.reload();
                    }
                    else{
                        $('#signError').text(arg.msg);
                    }
                }
            })
            }
            }
            )
    }

    function reply(){
        $('.fa-comment-dots').click(function(){
            $(this).parents('.single').after($('#reply-form').removeClass('d-none'));
            $('#reply-form').children('form').children('#reply_id').val($(this).parent().attr('id'));
        })
        $('.content').click(function(){
            $(this).after($('#reply-form').removeClass('d-none'));
            $('#reply-form').children('form').children('#reply_id').val($(this).attr('id'));
        })
        $('.content').hover(function(){
            $(this).children('.time').removeClass('d-none');
        },
            function(){
            $(this).children('.time').addClass('d-none');
            },
        )
    }

    function checkUsername(){

        $('#inputUsername').focus(function(){
                $('#usernameHelp').text('4-16位，可包含 数字 字母 _ -');
                $('#usernameHelp').attr('class','text-info');
                $('#usernameHelp').addClass('small');
        })

        $('#inputUsername').blur(function(){
            var username=$('#inputUsername').val();
            if(username){
                $.ajax({
                headers: {"X-CSRFToken":$.cookie("csrftoken")},
                url:'/check_username/',
                type:'POST',
                data:{'username':username},
                dataType:'JSON',
                success:function(arg){
                    if(arg.status){
                        $('#usernameHelp').text('该用户名可用');
                        $('#usernameHelp').attr('class','text-success');
                        $('#usernameHelp').addClass('small');
                        document.getElementById('inputUsername').setCustomValidity('');
                    }
                    else{
                        $('#usernameHelp').text('用户名已存在');
                        $('#usernameHelp').attr('class','text-danger');
                        $('#usernameHelp').addClass('small');
                        document.getElementById('inputUsername').setCustomValidity('用户名已存在');
                    }
                }
            })
            }
        })
    }
     function checkEmail(){
        $('#inputEmail').blur(function(){
            var str=$('#inputEmail').val();
            if(str){
                var re = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/;
                if (re.test(str)) {
                    $('#emailHelp').text('该邮箱可用');
                    $('#emailHelp').attr('class','text-success');
                    $('#emailHelp').addClass('small');
                    document.getElementById('inputUsername').setCustomValidity('');
                } else {
                    $('#emailHelp').text('邮箱格式错误');
                    $('#emailHelp').attr('class','text-danger');
                    $('#emailHelp').addClass('small');
                    document.getElementById('inputEmail').setCustomValidity('邮箱格式错误');
                }
            }
        })
        $('#inputEmail').focus(function(){
            $('#emailHelp').text('请输入你常用的邮箱');
            $('#emailHelp').attr('class','text-info');
            $('#emailHelp').addClass('small');
            document.getElementById('inputEmail').setCustomValidity('');
        })
      }

    function singleVerify(){
        $('#signButton').click(function(){
            var confirm=document.getElementById('confirmPassword');
            var p1=$('#inputPassword').val();
            var p2=$('#confirmPassword').val();
            if(p1!=p2){
                confirm.setCustomValidity("两次输入密码不一致");
            }
        })
    }