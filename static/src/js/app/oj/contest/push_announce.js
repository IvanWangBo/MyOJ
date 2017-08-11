require(["jquery", "bsAlert", "csrfToken", "validator"], function ($, bsAlert, csrfTokenHeader) {

	//TODO textarea width and height

	var btn_push = $("#btn_push_announce");

	btn_push.click(function(){

		var contest_id = $("#announce_ID").val();
		var content = $("#announce_content").val();

		$.ajax({
			beforeSend: csrfTokenHeader,
			url: "/api/push_contest_announcement/",
			data: {contest_id:contest_id, content:content},
			dataType: "json",
			method: "post",
			success: function (data) {
				if(!data.code){
					bsAlert(data.data);
				}
				else{
					bsAlert(data.data);
				}
			},
			error: function(){
				bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
			}

		});
	});

});
