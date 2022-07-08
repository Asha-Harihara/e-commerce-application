console.log('Hello')

var updateBtns=document.getElementsByClassName('update-cart')
{
    for(var i=0; i<updateBtns.length; i++)
    {
        updateBtns[i].addEventListener('click', function(){
          var productId=this.dataset.product
          var action=this.dataset.action
          console.log('productId:', productId, 'Action:', action)
          console.log('user:', user)

          updateUserCart(productId, action)
        })
    }

}

function updateUserCart(productId, action)
{
    console.log('User is authenticated ')
    var url='/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,

        },
        body:JSON.stringify({'productId':productId, 'action': action})
    }).then((response)=>{
       return response.json();
    }). then((data)=>{
        console.log('Data:', data)
        location.reload()
    })

}

var orderBtn=document.getElementsByClassName('do-order')
{
    
    for(var i=0; i<orderBtn.length; i++)
    {
    orderBtn[i].addEventListener('click', function(){

        var shippid=this.dataset.shippid
        console.log('user:', user)
        console.log('shipp:', shippid)
        if(shippid!=-1)
        doOrder(shippid)
    })
   }
}

function doOrder(shippid)
{  console.log('User is authenticated ')
var url='/orderItems/'
fetch(url, {
    method:'POST',
    headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken':csrftoken,

    },
    body:JSON.stringify({'shippid':shippid})
}).then((response)=>{
   return response.json();
}). then((data)=>{
    console.log('Data:', data)
    location.reload()
})

    
}



var updateQuant=document.getElementsByClassName('update-quant')
{
    for(var i=0; i<updateQuant.length; i++)
    {
          updateQuant[i].addEventListener('click', function(){
          var productId=this.dataset.product
          var action=this.dataset.action
          console.log('productId:', productId, 'Action:', action)
          console.log('user:', user)

          updateQuantity(productId, action)
        })
    }

}

function updateQuantity(productId, action)
{
    console.log('User is authenticated ')
    var url='/update_quant/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,

        },
        body:JSON.stringify({'productId':productId, 'action': action})
    }).then((response)=>{
       return response.json();
    }). then((data)=>{
        console.log('Data:', data)
        location.reload()
    })

}

var statusBtns=document.getElementsByClassName('update-status')
{
    for(var i=0; i<statusBtns.length; i++)
    {
         statusBtns[i].addEventListener('click', function(){
          var productId=this.dataset.product
          var action=this.dataset.action
          console.log('productId:', productId, 'Action:', action)
          console.log('user:', user)

          updateStatus(productId, action)
        })
    }

}
function updateStatus(productId, action)
{
   
    var url='/update_status/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,

        },
        body:JSON.stringify({'productId':productId, 'action': action})
    }).then((response)=>{
       return response.json();
    }). then((data)=>{
        console.log('Data:', data)
        location.reload()
    })

}