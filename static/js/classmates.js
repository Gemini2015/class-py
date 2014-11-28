function DeleteUser(id)
{
	// $.post(
	// 	"/deleteuser",
	// 	{userId:id},
	// 	function(data)
	// 	{
	// 		UpdateUserList(data);	
	// 	},
	// 	"json"
	// 	);
	$.getJSON(
		'/deleteuser',
		{ userid: id },
		function(data)
		{
			UpdateUserList(data);
		});
}

function UpdateUserList(data)
{

    jQuery.each(data,function(i, item){
        $('#infolist').children('#'+item.id).remove();
    });
    $('.btn-ctl-display').show();
    /*
	var ul = $('#infolist').empty();
	var userid = $('#userid').val();


	jQuery.each(data,function(){
		if(this.fields.user != userid && !this.fields.user.fields.is_superuser)
		{
			ul.append('<li> \
                <div class="row list-item"> \
                  <div class="col-lg-9"> \
                    <a href="/info/'+ this.fields.user.pk +'">'+ this.fields.cname +'</a>	\
                  </div>	\
                  <div class="col-lg-3 btn-ctl-display"> 	\
                    <button class="btn btn-sm btn-ctl-display" onclick="DeleteUser('+ this.fields.user.pk
                    	+')"><span class="glyphicon glyphicon-remove"></span></button> \
                  </div>	\
                </div>	\
              </li>');
		}
		else
		{
			ul.append('<li> \
                <div class="row list-item"> \
                  <div class="col-lg-9"> \
                    <a href="/info/'+ this.fields.user.pk +'">'+ this.fields.cname +'</a>	\
                  </div>	\
                  <div class="col-lg-3 btn-ctl-display"> 	\
                  </div>	\
                </div>	\
              </li>');
		}
	});
	$('.btn-ctl-display').show();
	*/
}

