function getStatus(url) {
    $.ajax({
        url: url,  
        type: 'Get',            
        success: function (data) {
        	for(var o in data){
        		var tag = "";
        		if (data[o].tag == 'vex_op'){
        			tag = "vex_";
        			$("#" + tag + "op_running_version_" + data[o].id).html(data[o].running_version);
        			$("#" + tag + "op_running_build_" + data[o].id).html(data[o].build_info);
        		}else if(data[o].tag == 'benchmark_op'){
        			tag = "benchmark_";
        		}
        		
        		//alert(data[o].name + ":" +data[o].status);
        		//alert(data[o].status == 1)
        		if (data[o].status == 1){
        			$("#" + tag + "op_status_" + data[o].id).html("Running");
        			$("#" + tag + "btn_start_" + data[o].id).hide();
        			$("#" + tag + "btn_stop_" + data[o].id).show();
        			$("#" + tag + "warm_up_minute_" + data[o].id).editable('disable');
        		}else if (data[o].status == 0){
        			$("#" + tag + "op_status_" + data[o].id).html("Stopped");
        			$("#" + tag + "btn_stop_" + data[o].id).hide();
        			$("#" + tag + "btn_start_" + data[o].id).show();
        			$("#" + tag + "warm_up_minute_" + data[o].id).editable('enable');
        		}else{
        			$("#" + tag + "op_status_" + data[o].id).html("");
        		}
            } 
        }  
    });  
} 

function ucfirst(str) {
	var str = str.toLowerCase();
	str = str.replace(/\b\w+\b/g, function(word){
	  return word.substring(0,1).toUpperCase()+word.substring(1);
	});
	return str;
}

function operation(op_tag, op_id, btn_id, is_vex_operation, test_type, update_status_message){
	var timeout = 300000;
	var btn = $("#" + btn_id);
	btn.button('loading');
	
	$.ajax({ 
           type: "get", 
           url: "/op/execute?op_tag=" + op_tag + "&op_id=" + op_id + "&vex_op=" + is_vex_operation,
           dataType: "json",
           timeout:timeout,
           success: function (data) { 
        	   if(data["status_code"] == 200){
        		   if (op_tag == "result"){
        			    window.location = "/result/" + test_type;
        		   }else{
	   					bootbox.alert({
	   						title: "<p><strong class='text-info'>" + ucfirst(op_tag) + " Succeed</p>",
	   						message: "<p><strong class='text-success'>" + data["message"] + "</p>",
	   					    size: 'large'
	   					});
	   					btn.button('reset');
	   					
	   					if(op_tag=="start" && update_status_message=="true"){
	   						$("#op_status_" + op_id).html("Running");
	   						$("#btn_start_" + op_id).hide();
	   						$("#btn_stop_" + op_id).show();
	   						
	   						try{ 
	   							$('#warm_up_minute_' + op_id).editable('disable');
	   						}catch (e) { 
	   						}
	   					}
	   					
	   					if(op_tag=="stop" && update_status_message=="true"){
	   						$("#op_status_" + op_id).html("Stopped");
	   						$("#btn_start_" + op_id).show();
	   						$("#btn_stop_" + op_id).hide();
	   						
	   						try{ 
	   							$('#warm_up_minute_' + op_id).editable('enable');
	   						}catch (e) { 
	   						}
	   					}
	   					
	   					getBasicCompontentStatus();
        	        }
   				}else{
   					bootbox.alert({
   						title: "<p><strong class='text-info'>" + ucfirst(op_tag) + " Failure</p>",
   						message: "<p><strong class='text-danger'>" + data["message"] + "</p>",
   					    size: 'large'
   					});
   					btn.button('reset');
   				}
           },
           error: function(){
        	   bootbox.alert({
   					title: "<p><strong class='text-info'>" + ucfirst(op_tag) + " Failure</p>",
   					message: "<p><strong class='text-danger'>Operation timeout. Please check status manually.</p>",
   				    size: 'large'
   				});
   				btn.button('reset');
           }
   });
}