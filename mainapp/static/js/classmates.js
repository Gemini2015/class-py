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
		{ userId: id },
		function(data)
		{
			UpdateUserList(data);
		});
}

function UpdateUserList(data)
{
	var ul = $('#userList').empty();
	var userId = $('#userId').val();

	jQuery.each(data,function(){
		if(this.pk != userId)
		{
			ul.append('<li> \
                <div class="row list-item"> \
                  <div class="col-lg-9"> \
                    <a href="/info/'+ this.pk +'">'+ this.fields.cname +'</a>	\
                  </div>	\
                  <div class="col-lg-3 btn-ctl-display"> 	\
                    <button class="btn btn-sm btn-ctl-display" onclick="DeleteUser('+ this.pk
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
                    <a href="/info/'+ this.pk +'">'+ this.fields.cname +'</a>	\
                  </div>	\
                  <div class="col-lg-3 btn-ctl-display"> 	\
                  </div>	\
                </div>	\
              </li>');
		}
	});
	$('.btn-ctl-display').show();
}

