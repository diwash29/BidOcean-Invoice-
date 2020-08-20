$(function(){
	$('.in input').change(function(){
		var p=$(this).parent().parent()
		var m=p.find('input.txtMult')
		var mul=parseFloat($(m[0]).val()*$(m[1]).val()).toFixed(2)
		var res=p.find('.multTotal')
		res.html(mul);
		var total=0;
		$('.in .multTotal').each(function(){
			total+=parseFloat($(this).html())
		})
		$('.in #grandTotal').html(parseFloat(total).toFixed(2))
	});
})