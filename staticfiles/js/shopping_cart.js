// import Pizza from  './Pizza.js'

async function getItemData(id) {
    console.log('Getting data');    
    const res = await fetch(`/shop/delete/shopping-item/${id}`);
    const data = await res.json();        
    return data;    
}


const deleteCartItemButtons = document.querySelectorAll('.btn-delete-cart-item');
const confirmOrderButton = document.querySelector('#place-order')


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
        return cookieValue;
    }
}

const CSRF = () => {
    let csrftoken = getCookie('csrftoken');
    return (
        <input type='hidden' name="csrfmiddlewaretoken" value={csrftoken} id='csrftoken' />
    )
}


const StatusMessage = ({data}) => {
    return (
        <div className="row px-sm-4 px-2 fs-1 text-center">
            {/(order|deleted)/ig.test(data.message)? 
            (
             <p className="col-10 offset-1 text-center">
                 <i className="fas fa-check-circle fa-5x"></i>
             </p>   
            
        ):
                (
                    <p className="col-10 offset-1 text-center">
                        <i className="fas fa-times-circle fa-5x"></i>
                    </p>   )
        }
            <p className="col-10 offset-1 text-center fs-1">
                {data.message}                
            </p>   
            <p className="col-10 offset-1 text-center fs-3">
                {data.email? (<span>Order information sent to {data.email}</span>): ""}
            </p>
            
        </div>
    )
}

function ShoppingModal() {
    let [confirmDelete, setConfirmDelete] = React.useState(false);
    let [confirmOrders, setConfirmOrders] = React.useState(false)
    let [itemId, setItemId] = React.useState(0)    
    let [data, setData] = React.useState(null);
    let [status, setStatus] = React.useState(null)
    
    React.useEffect(() => {                      
        
        deleteCartItemButtons.forEach((btn) => {                
            btn.onclick = async () => {                                      
                const item = await getItemData(btn.dataset.itemid);                                
                console.log('data', item)
                setData(item);                                                            
                setItemId(btn.dataset.itemid)
                setConfirmDelete(true)                                
            }    
        });

        if (confirmOrderButton) {
            confirmOrderButton.onclick = async () => {
                let res = await fetch('/shop/view-cart/data/', {
                    method: 'GET'
                })
                let cartItems = await res.json()                
                setData(cartItems)
                setConfirmOrders(true)
            }
        }
        
    }, []);

    const deleteShoppingCartItem = React.useCallback(async (id) => {                
        if (!data.error) {
            let csrf = document.querySelector('#csrftoken').value
            let res = await fetch(`/shop/delete/shopping-item/${id}/`, {
                method: "DELETE",                
                headers: {                  
                    'X-CSRFToken': csrf,
                },                
            });
            let data = await res.json()
            
            setStatus(data)
            setConfirmDelete(false)
        }        
    }, [data]);

    const addShoppingItemsToOrder = React.useCallback(async () => {
        if (!data.error) {
            let csrf = document.querySelector('#csrftoken').value
            let res = await fetch(`/order/add-cart-items/`, {
                method: "POST",                
                headers: {                  
                    'X-CSRFToken': csrf,
                },                
            });
            let data = await res.json()
            
            setStatus(data)
            setConfirmOrders(false)
        }        
    })
    
    return (
        <div>
        <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content modal-background-color text-white">
                    <div className="modal-header">
                            {
                             confirmDelete && <h2 className="modal-title text-center col-12"> Delete From Cart? </h2>
                            }     
                            
                    </div>
                <div className="modal-body px-0" id="modal-content">
            
                
                    <div className="container-fluid">                       
                            {confirmDelete && 
                                <div className="row">
                                    <ShoppingCartMessage data={data} />
                                </div>
                            }                      
                            {confirmOrders && 
                                <div className="row">
                                    <ConfirmOrdersMessage data={data} />
                                </div>
                            }
                    </div>
                </div>
                {confirmDelete &&

                    <div className="d-grid gap-2 modal-footer-modified">                    
                        <button onClick={() => {setData(null); setConfirmDelete(false)}} type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" className="btn btn-danger" id="delete-item" onClick={() => {deleteShoppingCartItem(itemId);}}>Delete</button>
                    </div>
                }     
                {confirmOrders &&

                    <div className="d-grid gap-2 modal-footer-modified">                    
                        <button onClick={() => {setData(null); setConfirmOrders(false)}} type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" className="btn btn-success" id="add-orders" onClick={() => {addShoppingItemsToOrder()}}>Place Order</button>
                    </div>
                }     



                {status &&  
                    <StatusMessage data={status} />
                }      
                { status && 
                <div className="d-grid gap-2 modal-footer-modified">                                    
                    <button type="button" className="btn btn-success" id="confirm-action" onClick={() => { setTimeout(() => {setStatus(null); window.location.reload()}, 100)}} data-bs-dismiss="modal">OK</button>
                </div> }
                                        
            </div>
        </div>
        </div>
    )
}

ReactDOM.render(<ShoppingModal />, document.querySelector('#shoppingCartModal'));

const ShoppingCartMessage = ({data}) => {        
    
    return (
        <div className="col-12 px-sm-4 px-2">
            <CSRF />
            <table className="row col-12 table table-dark" id="delete-orders-confirm">
                
                    { data &&  
                    
                    <tbody className="py-3">
                    <tr>
                        <td colSpan="3" className="text-start"><h2>{data.food_item}</h2></td>
                    </tr>
                    <tr>
                        <td colSpan="3" className="fs-5 text-start"><p>{data.choices}</p></td>
                    </tr>
                    <tr>
                        <td colSpan="2" className="fs-5 text-start">Total</td>                        
                        <td className="text-end fs-4" style={{fontFamily: 'Arial'}}><p>= ${data.price}</p></td>
                    </tr>
                    </tbody>
                    }                
            </table>
        </div>
    )
}

const ConfirmOrdersMessage = ({data}) => {        
    
    return (
        <div className="col-12 px-sm-4 px-2">
            <CSRF />
            <h2 className="modal-title text-center col-12">Placing Order</h2>
            <table className="col-12 table" id="order-confirm-table">
                
                    { data &&  
                    
                    <tbody>
                        {data.shopping_cart.map((item, id) => {
                            return (
                            <React.Fragment key={id}>
                                <tr>
                                    <td colSpan="3">
                                <table className="col-12 table" id="table-orders-confirm">
                                <tbody>
                                    <tr>
                                        <td colSpan="3" className="text-start"><h2>{item.food_item}</h2></td>
                                    </tr>
                                    <tr>
                                        <td colSpan="3" className="fs-5 text-start"><p>{item.choices}</p></td>
                                    </tr>
                                    <tr>
                                        <td colSpan="2" className="fs-5 text-start">Price</td>                        
                                        <td className="text-end fs-5 px-2" style={{fontFamily: 'Arial'}}><p>= ${item.price}</p></td>
                                    </tr>
                                </tbody>
                                </table>
                                </td>
                                </tr>
                                
                            </React.Fragment>
                            )
                        })}
                        <tr id="orders-total-confirm">
                                    <td colSpan="2" className="fs-5 text-start">Total</td>                        
                                    <td className="text-end fs-4" style={{fontFamily: 'Arial'}}><p className="px-2">= ${data.total_price}</p></td>
                        </tr>
                    
                    </tbody>
                    }                
            </table>
        </div>
    )
}