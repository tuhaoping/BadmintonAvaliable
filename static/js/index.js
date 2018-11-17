$("#sc-chooseall").click(function(){
  console.log($(this).prop('checked'))
  if ($(this).prop('checked'))
    $(".ckb.sc-item").addClass('disabled').find('input').prop('disabled', true)
  else
    $(".ckb.sc-item").removeClass('disabled').find('input').prop('disabled', false)
})