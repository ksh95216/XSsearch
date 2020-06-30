function search(){
          
    var url = $("#url").val();
    var chk = $("#chk").is(":checked");
    var cookie = $("#cookie").val();
    $.ajax({

        type:"POST"
        ,url: "/api/search"
        ,data :{ url: url, use_cookie: chk, cookie: cookie }
        ,success: function(res){

	    res = JSON.parse(res)
	    console.log(res)
	    if(res.success == 'false'){

		return alert(res.msg);

	    }

            get_vuln(res)
	    $('#Result_modal').modal('show');

        }
        ,beforeSend:function(){
    
            $('.wrap-loading').removeClass('display-none');

        }
        ,complete:function(){

            $('.wrap-loading').addClass('display-none');
        }

        ,error:function(e){

            //조회 실패일 때 처리

        }
    });
}

function login(){ 

	var username = $("#Lusername").val(); 
	var password = $("#Lpassword").val();

	$.ajax({

     		type:"POST"
        	,url: "/api/login"
        	,data :{ username: username, password: password}
        	,success: function(res){

			res = JSON.parse(res)
			console.log(res)
			if(res.success == 'true'){

				alert(res.msg);
				location.reload();
			
			}
			else{

				alert(res.msg);		

			}
	
	        }

	});
}
function Register(){

        var username = $("#Rusername").val();
        var password = $("#Rpassword").val();

        $.ajax({

                type:"POST"
                ,url: "/api/register"
                ,data :{ username: username, password: password}
                ,success: function(res){

			
			res = JSON.parse(res)
			console.log(res)
                        if(res.success == 'true'){

                                alert(res.msg);
				$('#Register_modal').modal('hide');$('#Login_modal').modal('show');
				return true;

                        }
                        if(res.success == 'false'){

                                alert(res.msg);
				return false;		

                        }

                }

        });
}

function get_vuln(xs){

	p = new RegExp("_XS_.*?['\"<>]+.*?_XS_")
	div = "<div><br>"
	
	xs.forEach(function(element){
		
		for(var key in element){

			if(key != 'line'){
				console.log(p.exec(element[key]))
				if(p.exec(element[key])){
				
					find = p.exec(element[key])[0].replace(/\</gi,"&lt;").replace(/\>/,"&gt;");
					data = element[key].replace(/\</gi,"&lt;");
					data = data.replace(/\>/gi,"&gt;");
					data = (element['line']+1)+" | " +data.replace(find,"<span class='vuln' style='color: red;'>"+find.replace(/&/g, "&amp;")+"</span>");
					data = '<div>Parameter: '+key+' </div><div>Type: Vulnerablity!</div><pre class="line-numbers"><code class="language-markup">'+data+' </code> </pre>';
					div += data
				}

			}

		}

	});
	div += "<br></div>"
	console.log(div)

	if(div == "<div><br><br></div>")
		div = "<div><br><div style='text-align:center;'>Not Found!</div><br></div";

	$('.Result_modal-body').html(div)


}
function GetLoginInfo(){

	$.ajax({
 	
		type:"GET"
                ,url: "/api/status"
                ,success: function(res){

			res = JSON.parse(res)
			console.log(res)

			if(res.success == true){

				$('#login_out').html("<i class='fas fa-sign-out-alt'></i> Logout");
				$('#login_out').attr("onclick","logout()");
				return true;				

			}
		}

	});

}
function logout(){

	$.ajax({

		type:"GET",
		url: "/api/logout",
		success: function(res){

			res = JSON.parse(res);
			alert(res.msg);
			location.reload();

		}
	});
	

}

function Report(){

        var url = $("#Rurl").val();

        $.ajax({

                type:"POST"
                ,url: "/api/report"
                ,data :{ url:url}
                ,success: function(res){

                        res = JSON.parse(res)
			if(res.success == "true"){

				alert(res.msg);
				location.reload();
				return true;
			}
			else{

				alert(res.msg);
				return false;

			}
                        console.log(res)
                }

        });
}

function cookie_box(){

    var chk = document.getElementById('chk');

    if(chk.checked == true){
            
        document.getElementById('cookie').setAttribute('class', 'cookieTerm');
                        
    }
    else{

        document.getElementById('cookie').setAttribute('class', 'cookieTerm display-none');
  
   }
}

GetLoginInfo();
