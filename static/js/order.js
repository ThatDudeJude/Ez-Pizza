// import Pizza from  './Pizza.js'

async function getItemData(orderItem, id) {
    console.log('Getting data');    
    const res = await fetch(`/order/${orderItem}/${id}`);
    const data = await res.json();        
    return data;    
}

async function specialItemData(orderItem) {
    console.log('Getting Special data');    
    const res = await fetch(`/order-special/${orderItem}/`);
    const data = await res.json();        
    return data;    
}

const regularButtons = document.querySelectorAll('.pizza-regular-button');
const regularSpecialButton = document.querySelectorAll('.regular-special-button');
const sicillianSpecialButton = document.querySelectorAll('.sicillian-special-button');
const sicillianButtons = document.querySelectorAll('.pizza-sicillian-button')        
const subButtons = document.querySelectorAll('.sub-button');
const pastasButton = document.querySelector('#pasta-button');
const saladsButton = document.querySelector('#salad-button');
const platterButtons = document.querySelectorAll('.platter-button');

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

const getShoppingItemsCount = async () => {
    let res = await fetch("/shop/shopping-cart/")
    let data = await res.json()            
    document.querySelector('.shopping-cart').dataset.count =  data.items
}

getShoppingItemsCount();


const SubmittedMessage = ({data}) => {    

    React.useEffect(async () => {        
        console.log('submitting order', data.error);
        if (!data.error) {
            let csrf = document.querySelector('#csrftoken').value
            await fetch('/shop/add-order-item/', {
                method: "POST",                
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body: JSON.stringify(data.message)
            });
        }
        getShoppingItemsCount();                
    }, [data]);
    
    return (
        <div className="col-12 px-sm-4 px-2">
            <CSRF />
            <table className="col-12 table">
                
                    {data.error ? 
                    <tbody>
                    <tr>
                    <td colSpan="3" className="text-start"><h2>{data.message}</h2></td>
                    </tr>
                    </tbody>
                    :
                    <tbody>
                    <tr>
                        <td colSpan="3" className="text-start"><h2>{data.message.food}</h2></td>
                    </tr>
                    <tr>
                        <td colSpan="3" className="fs-5 text-start"><p>{data.message.info}</p></td>
                    </tr>
                    <tr>
                        <td colSpan="2" className="fs-5 text-start">Total</td>                        
                        <td className="text-end fs-4" style={{fontFamily: 'Arial'}}><span>= ${data.message.price}</span></td>
                    </tr>
                    </tbody>
                    }                
            </table>                                    
        </div>
    )
}

function OrderForm() {
    const [order, setOrder] = React.useState('');
    const [orderInfo, setOrderInfo] = React.useState({});
    const [priceAvailable, setPriceAvailable] = React.useState(false);
    const [form, setForm] = React.useState(null);
    const [submitted, setSubmitted] = React.useState(null);


    
    // const [id, setId] = React.useState(0);
    // const formData = React.useMemo(
    //     () => getItemData(order, id), [order, id]
    // )
    
    React.useEffect(() => {                      
        regularButtons.forEach((btn, idx) => {                
            btn.onclick = async () => {                      
                const data = await getItemData('regular', btn.dataset.shopitemid);
                // console.log(data);            
                setOrderInfo(data);
                setOrder('pizza');      
                // console.log('orderInfo', orderInfo);
            }    
        });
        regularSpecialButton.forEach((btn) => {                
            btn.onclick = async () => {                      
                const data = await specialItemData('regular');
                // console.log(data);            
                setOrderInfo(data);
                setOrder('pizza');      
                // console.log('orderInfo', orderInfo);
            }    
        });
        sicillianSpecialButton.forEach((btn) => {                
            btn.onclick = async () => {                      
                const data = await specialItemData('sicillian');
                // console.log(data);            
                setOrderInfo(data);
                setOrder('pizza');      
                // console.log('orderInfo', orderInfo);
            }    
        });
        
        sicillianButtons.forEach((btn, idx) => {                            
            btn.onclick = async () => {                          
                const data = await getItemData('sicillian', btn.dataset.shopitemid);                
                setOrderInfo(data);
                setOrder('pizza');      
                // console.log('orderInfo', orderInfo);
            }    
        });
        subButtons.forEach((btn, idx) => {                            
            btn.onclick = async () => {                          
                const data = await getItemData('subs', btn.dataset.shopitemid);                
                setOrderInfo(data);
                setOrder('subs');      
                // console.log('orderInfo', orderInfo);
            }    
        });
        pastasButton.onclick = async () => {
            const data = await getItemData('pastas', 0);
            console.log('pastas', data);
            setOrderInfo(data);
            setOrder('pastas');  
            
        }
        saladsButton.onclick = async () => {
            const data = await getItemData('salads', 0);
            console.log('salads', data);
            setOrderInfo(data);
            setOrder('salads');  
            
        }
        platterButtons.forEach((btn, idx) => {                            
            btn.onclick = async () => {                          
                const data = await getItemData('platters', btn.dataset.shopitemid);                
                setOrderInfo(data);
                setOrder('platters');      
                // console.log('orderInfo', orderInfo);
            }    
        });
        
    }, []);

    const submitForm = React.useCallback(async () => {
        const data = {"item": form.dataset.food}
        document.querySelectorAll('input').forEach( child => {
            if (child.nodeName == 'INPUT' && (child.checked ||                 
                /(csrfmiddlewaretoken|topping|type|special)/i.test(child.name))
                ) {
                let name = child.name, value = child.value; data[name] = value;
            }
        })
        // console.log('form data', data)    
                    
        let res = await fetch(form.action, {
            credentials: 'include', 
            method: 'POST',
            mode: 'same-origin',
            headers: {
                'Accept':'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': data['csrfmiddlewaretoken']
            },
            body: JSON.stringify(data)
        });
        res = await res.json()
        setSubmitted(res)
        // console.log('form data', data, res)                
    }, [form])
    
    
    
    return (
        <div>
        <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content modal-background-color text-white">
                    <div className="modal-header">
                            <h2 className="modal-title text-center col-12">{
                            submitted ? 'Placed Order': (orderInfo && orderInfo.name)}
                            {submitted ? '' :
                                <button onClick={() => {setOrderInfo({}); setOrder(''); setPriceAvailable(false)}} style={{color: 'white'}} type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close">
                                    <span onClick={() => {setOrderInfo({}); setOrder(''); setPriceAvailable(false)}} style={{color: 'white'}} aria-hidden="true">&times;</span>
                                </button>
                            }
                            </h2>
                    </div>
            <div className="moif(pizzaTotalP)dal-body px-0" id="modal-content">
            
        {/* <h3 style={{width: '100%', textAlign: 'center', marginBottom: '20px'}}> </h3> */}
              <div className="container-fluid">                       
                    {submitted ? <SubmittedMessage data={submitted} /> :
                      <div className="row px-1 px-sm-2">
                          {(order == 'pizza' && orderInfo != {}) ?  <Pizza data={orderInfo.data} toppings={orderInfo.toppings} name={orderInfo.name} checkPrice={setPriceAvailable} getForm={setForm} /> : ''}
                          {(order == 'subs' && orderInfo != {}) ?  <Sub data={orderInfo.data}  name={orderInfo.name} checkPrice={setPriceAvailable} getForm={setForm} /> : ''}
                          {(order == 'pastas' && orderInfo != {}) ?  <Pasta data={orderInfo.data}  name={orderInfo.name} checkPrice={setPriceAvailable} getForm={setForm} /> : ''}
                          {(order == 'salads' && orderInfo != {}) ?  <Salad data={orderInfo.data}  name={orderInfo.name} checkPrice={setPriceAvailable} getForm={setForm} /> : ''}
                          {(order == 'platters' && orderInfo != {}) ?  <Platter data={orderInfo.data}  name={orderInfo.name} checkPrice={setPriceAvailable} getForm={setForm} /> : ''}
                      </div>
                    }
              </div>
              </div>
              {submitted ?  
                <div className="d-grid gap-2 modal-footer-modified">                                    
                    <button type="button" className="btn btn-success" id="confirm" onClick={() => { setTimeout(() => {setSubmitted(null);  setPriceAvailable(false); setOrder('')}, 100)}} data-bs-dismiss="modal">OK</button>
                </div>
              : 
                <div className="d-grid gap-2 modal-footer-modified">                    
                    <button onClick={() => {setOrderInfo({}); setOrder(''); setPriceAvailable(false)}} type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" className="btn btn-success" id="add" disabled={!priceAvailable} onClick={() => submitForm()}>Add to Cart</button>
                </div>
                }
            </div>
        </div>
        </div>
    )
}

ReactDOM.render(<OrderForm />, document.querySelector('#addItemModal'));

const toppingsReducer = (state, action) => {
    switch (action.type) {
        case 'UPDATE_AVAILABLE_TOPPINGS':
            let choices = Object.values(action.payload.choices)                
            return {toppings: [...action.payload.toppings].filter(t => !choices.includes(t.name)), 'choices': action.payload.choices};
        case 'SET_TOPPINGS':

            return {toppings: action.payload.toppings, choices: action.payload.choices};
        default:
            return state;
    }
}



const Pizza = ({data, toppings, name, checkPrice, getForm}) => {

    let [availToppings, updateToppings] = React.useReducer(toppingsReducer, {'toppings': toppings, 'choices': {
        'topping1': '',
        'topping2':'',
        'topping3':''
    }});

    let [total, updateTotal] = React.useState('00.00');    
    let smallRef = React.useRef();
    let largeRef = React.useRef();

    React.useEffect(() => {
        updateToppings({type:'SET_TOPPINGS', payload: {'toppings': toppings, 'choices': availToppings.choices}})
        // smallRef.current.checked = false;
        // largeRef.current.checked = false;
    }, [toppings]);
    
    // console.log('tops', toppings, 'avail', availToppings.toppings, 'choices', availToppings.choices);

    

    const onSelectToppingOne = React.useCallback(() => {
        const value = document.querySelector('#toppingOne').value;        
        const choices = {...availToppings.choices, 'topping1': value};
        // console.log('choices change 1', choices)
        updateToppings({type:'UPDATE_AVAILABLE_TOPPINGS', payload: {toppings, choices}});
    }, [availToppings]);

    const getTotalPrice = React.useCallback(() => {
        let choices = [smallRef, largeRef];
        let pizzaTotalPrice = 0;

        choices.forEach(choice => {
            if (choice.current.checked) {
                pizzaTotalPrice += parseFloat(choice.current.value);
            }
        });
        
        if (pizzaTotalPrice === 0) pizzaTotalPrice = '00.00'
        updateTotal(toDecimalPlaces(String(pizzaTotalPrice), 2).padStart(6));
               
        checkPrice(pizzaTotalPrice != 0)
        checkPrice((smallRef.current.checked || largeRef.current.checked))
        getForm(document.querySelector(name.includes('Regular')? "#regular-form": "#sicillian-form"))
    }, [])

    const onSelectToppingTwo = React.useCallback(() => {
        const value = document.querySelector('#toppingTwo').value;
        const choices = {...availToppings.choices, 'topping2': value};
        // console.log('choices change 2', choices)
        updateToppings({type:'UPDATE_AVAILABLE_TOPPINGS', payload: {toppings, choices}});
    }, [availToppings]);

    const onSelectToppingThree = React.useCallback(() => {
        const value = document.querySelector('#toppingThree').value;
        const choices = {...availToppings.choices, 'topping3': value};
        // console.log('choices change 3', choices)
        updateToppings({type:'UPDATE_AVAILABLE_TOPPINGS', payload: {toppings, choices}});
    }, [availToppings]);

    

    return (
      <div>          
                          <form action="/shop/add/pizza/" method="post" className='col-12 form-table-red py-3 px-2 mb-3' id={name.includes('Regular')? "regular-form": "sicillian-form"} data-food={name.includes('Regular')? "Regular Pizza": "Sicillian Pizza"}>   

                            <CSRF />
                        {data && data.special? (<h3 className="mb-2 text-center">Special</h3>)
                        : (<h3 className="mb-4 text-center">{data.delicacy}</h3>) }
                        {data && data.special ? (<h5 className="mb-4">{data.delicacy}</h5>): ''}

                        
                          
                          {data && !(/[123]/.test(data.delicacy)) && 
                              <input type='hidden' name="type" value={data.delicacy} />}    
                        {data && data.special && <input type="hidden" name="special" value="Special: "/>}                      
                          <table className="table" id="table-form">                                        
                                        <tbody>
                                            
                              
                              {data && /[123]/.test(data.delicacy) &&
                              <tr>                                  
                                  <td className="text-center"><label htmlFor="toppingOne" className="form-label fs-4 px-0">{name.includes('Regular') ? 'Topping 1' : 'Item 1'}</label></td>                                                                    
                                  <td colSpan="2">
                                      <input type="text" className="form-control fs-4 fs topping" name="toppingOne" id="toppingOne" list="topping1-options" onChange={() => onSelectToppingOne()}                                 
                                  defaultValue={availToppings.toppings? availToppings.toppings[0].name: ''} />
                                  <datalist  id="topping1-options">
                                  {availToppings.toppings? availToppings.toppings.map(topping => (<option key={topping.id}  value={topping.name} />)): ''}                                                                        
                                  </datalist>
                                  </td>                                  
                              </tr>
                                }

                                {data && /[23]/.test(data.delicacy) &&    
                            <tr>                                
                                <td className="text-center"><label htmlFor="toppingTwo" className="form-label fs-4 px-0">{name.includes('Regular') ? 'Topping 2' : 'Item 2'}</label></td>
                                <td colSpan="2"><input type="text" className="form-control fs-4 topping" name="toppingTwo" id="toppingTwo" list="topping2-options" onChange={() => onSelectToppingTwo()} 
                                defaultValue={availToppings.toppings? availToppings.toppings[0].name: ''} />
                                <datalist  id="topping2-options">
                                {availToppings.toppings? availToppings.toppings.map(topping => (<option key={topping.id}  value={topping.name} />)): ''}                                                                        
                                </datalist>
                                </td>                                
                                
                            </tr>
                                }

                                {data && /[3]/.test(data.delicacy) &&
                                <tr>                                  
                                  <td className="text-center"><label htmlFor="toppingThree" className="form-label fs-4 px-0">{name.includes('Regular') ? 'Topping 3' : 'Item 3'} </label></td>
                                  <td colSpan="2"><input type="text" className="form-control fs-4 topping" name="toppingThree" id="toppingThree" list="topping3-options"onChange={() => onSelectToppingThree()} 
                                  defaultValue={availToppings.toppings? availToppings.toppings[0].name: ''} />
                                  <datalist  id="topping3-options">
                                    
                                  {availToppings.toppings? availToppings.toppings.map(topping => (<option key={topping.id}  value={topping.name} />)): ''}                                                                        
                                  </datalist>
                                  </td>                                  
                                </tr>
                                }

                              <tr>
                                  <td className="text-center">
                                      <input ref={smallRef} className="form-check-input" type="checkbox" name="small" id="small" onChange={() => getTotalPrice()} value={data? data.small: '00.00'} />
                                       </td>
                                  <td className="text-center">
                                      <label className="form-check-label fs-4" htmlFor="small">Small</label>                                                            </td>
                                  <td className="text-end"><p className="price fs-4 px-1">
                                       {data && data.small}
                                  </p></td>                                  
                              </tr>
                            <tr>
                                  <td className="text-center"><input ref={largeRef} className="form-check-input" type="checkbox" name="large" id="large" onChange={() => getTotalPrice()} value={data? data.large: '00.00'} /> </td>
                                  <td className="text-center"><label className="form-check-label fs-4" htmlFor="large">Large</label>                                                            </td>
                                  <td className="text-end"><p className="price fs-4 px-1">
                                       {data && data.large}
                                  </p></td>                                  
                              </tr>
                              
                              
                                <tr>                                    
                                    <td colSpan="2">
                                        <span className="fs-4" style={{fontFamily: 'Arial'}}>Total ($)</span>
                                    </td>                                  
                                    <td className="text-end">
                                        <span className="fs-4 px-1">= {total}</span></td>
                                </tr>   
                                </tbody>
                            </table>                             
                          </form>              
      </div>
    )
  }

function toDecimalPlaces(num, places) {
    let str = String(num).includes('.')? String(num): String(num) + '.';
    return str.split('.')[1].length == places ? str: parseFloat(str).toFixed(places);
}

const Sub = ({data, checkPrice,name, getForm}) => {

    let [total, updateTotal] = React.useState('00.00');  
    let [disableExtras, setDisableExtras] = React.useState(true)
    

    let smallRef = React.useRef();
    let largeRef = React.useRef();
    let cheese = React.useRef();
    
    let mushrooms = React.useRef();
    let peppers = React.useRef();
    let onions = React.useRef();        

    const getTotalPrice = React.useCallback(() => {
        const choices = [smallRef, largeRef];
        let subTotalPrice = 0

        const extras = data && /(Steak [+] Cheese)/i.test(data.sub) ? [
            cheese.current.checked, 
            mushrooms.current.checked, 
            peppers.current.checked, 
            onions.current.checked
        ]: [ cheese.current.checked]

        const extrasPrice = Object.values(extras).reduce((a, b) => a + b)  *  0.50;
        console.log('extras', extrasPrice);
        choices.forEach((choice, id) => {
            if (choice.current.checked) {
                
                subTotalPrice += parseFloat(choice.current.value);
                console.log(choice.current.value, subTotalPrice)
                
            }
            if (id == 1 && subTotalPrice !== 0) subTotalPrice += extrasPrice;
        })

        if (subTotalPrice === 0) subTotalPrice = '00.00'
        updateTotal(toDecimalPlaces(String(subTotalPrice), 2).padStart(6));
        setDisableExtras(!(smallRef.current.checked || largeRef.current.checked))
        checkPrice((smallRef.current.checked || largeRef.current.checked))
        getForm(document.querySelector("#sub-form"));
    }, [])   

    return (
        <form action="/shop/add/sub/" method="post" className='col-12 form-table-red py-3 px-2 mb-3' id="sub-form" data-food="Sub Sandwich">   
        <CSRF />
        <h3 className="mb-4 text-center">{data.sub}</h3>    
        <input type='hidden' name="type" value={data.sub} />
        <table className="table" id="table-form">                                        
                                        <tbody>
                
            <tr>
                <td className="text-center">
                <input ref={smallRef} className="form-check-input" type="checkbox" name="small" id="small" onChange={() => getTotalPrice()} value={data? data.small: '00.00'} /> 
                </td>
                <td className="text-center">
                <label className="form-check-label fs-4" htmlFor="small">Small</label>                                                            
                </td>
                <td className="text-end">
                <p className="price fs-4">
                     {data && data.small}
                </p>
                </td>
                                            
            </tr>
            <tr>
                <td className="text-center">
                <input ref={largeRef} className="form-check-input" type="checkbox" name="large" id="large" onChange={() => getTotalPrice()} value={data? data.large: '00.00'} /> 
                </td>
                <td className="text-center">
                <label className="form-check-label fs-4" htmlFor="large">Large</label>                                                            
                </td>
                <td className="text-end">
                <p className="price fs-4">
                     {data && data.large}
                </p>
                </td>
                
            </tr>
            
            {data && /(Steak [+] Cheese)/i.test(data.sub) &&
              <tr>
                <td className="text-center">
                <input ref={mushrooms} className="form-check-input" type="checkbox" name="+ Mushrooms" id="mushrooms" disabled={disableExtras} onChange={() => getTotalPrice()} value='0.50' />     
                </td>
                <td className="text-center">
                <label className="form-check-label fs-5" htmlFor="mushrooms">+Mushrooms</label>                                                            
                </td>
                <td className="text-end">
                <p className="price fs-4">
                    0.50
                </p>
                </td>
                
              </tr>
                }
            {data && /(Steak [+] Cheese)/i.test(data.sub) &&
              <tr>
                <td className="text-center">
                <input ref={peppers} className="form-check-input" type="checkbox" name="+ Green Peppers" id="green-peppers" disabled={disableExtras} onChange={() => getTotalPrice()} value='0.50' />       
                </td>
                <td className="text-center">
                <label className="form-check-label fs-5" htmlFor="green-peppers">+Green Peppers</label>                                                            
                </td>
              <td className="text-end">
              <p className="price fs-4">
                  0.50
              </p>
              </td>              
            </tr>
            }   
            {data && /(Steak [+] Cheese)/i.test(data.sub) &&
            <tr>
                <td className="text-center">
                <input ref={onions} className="form-check-input" type="checkbox" name="+ Onions" id="onions" disabled={disableExtras} onChange={() => getTotalPrice()} value='0.50' /> 
                </td>
            <td className="text-center">
            <label className="form-check-label fs-5" htmlFor="onions">+Onions</label>                                                            
            </td>
            <td className="text-end">
            <p className="price fs-4">
                0.50
            </p>
            </td>
            
          </tr>
              }

            <tr>
                <td className="text-center">
                <input ref={cheese} className="form-check-input" type="checkbox" name="+ Extra Cheese" id="cheese" disabled={disableExtras} onChange={() => getTotalPrice()} value='0.50' /> 
                </td>
            <td className="text-center">
            <label className="form-check-label fs-5" htmlFor="cheese">+Extra Cheese</label>                                                            
            </td>
            <td className="text-end">
            <p className="price fs-4">
                0.50
            </p>
            </td>
            
          </tr>
            
              <tr>
                  <td colSpan="2">
                  <span className="fs-4" style={{fontFamily: 'Arial'}}>Total ($)</span>                                  
                  </td>
                  <td className="text-end">
                  <span className="fs-4">= {total}</span>
                  </td>
                  
              </tr>   

              </tbody>
              </table>                         
              
        </form>              
    )
}

const Pasta = ({data, checkPrice, name, getForm}) => {

    let [total, updateTotal] = React.useState('00.00');  
        
    let mozzarellaRef = React.useRef();
    let meatballsRef = React.useRef();
    let chickenRef = React.useRef();         

    const getTotalPrice = React.useCallback(() => {
        let pastas = [mozzarellaRef, meatballsRef, chickenRef];
        let pastasTotal = 0
        pastas.forEach(pasta => {
            if (pasta.current.checked) {
                pastasTotal += parseFloat(pasta.current.value)
            }
        })   
        
        if (pastasTotal === 0) pastasTotal = '00.00'
        updateTotal(toDecimalPlaces(String(pastasTotal), 2).padStart(6));
           
        checkPrice(pastasTotal != 0)
        getForm(document.querySelector("#pasta-form"))
    }, []);

    
    return (
        <form action="/shop/add/pasta/" method="post" className='col-12 form-table-red py-3 px-2 mb-3' id="pasta-form" data-food="Pasta">   
            <CSRF />
            <table className="table" id="table-form">                                        
                                        <tbody>

            {data && data.map((pasta, id) => {
                let refPasta, name, fullName;                
                console.log(pasta.delicacy)
                if (/Mozzarella/i.test(pasta.delicacy)) {
                    refPasta = mozzarellaRef;
                    name = "mozzarella-price"
                    fullName = "Baked Ziti w/ Mozzarella"
                    
                } else if (/Meatballs/i.test(pasta.delicacy)) {
                    refPasta = meatballsRef;
                    name = "meatballs-price"
                    fullName = "Baked Ziti w/ Meatballs"
                    
                } else if (/Chicken/i.test(pasta.delicacy)) {
                    refPasta = chickenRef;
                    name = "chicken-price"
                    fullName = "Baked Ziti w/ Chicken"
                }
            return (
                <tr key={id}>
                <td className="text-center">                
                <input ref={refPasta} className="form-check-input" type="checkbox" name={fullName} id={name} onChange={() => getTotalPrice()} value={data && pasta.fixed} /> 
                </td>
                <td className="text-center px-0">
                <label className="form-check-label fs-5 pasta-label" htmlFor={name}>{pasta.delicacy}</label>                                                            
                </td>
                <td className="text-end">
                <span className="price fs-5 px-2">
                     {data && pasta.fixed}
                </span>
                </td>                
            </tr>
            )
        })
        }                      
              <tr>
                  <td colSpan="2" className="text-center">
                  <span className="fs-4" style={{fontFamily: 'Arial'}}>Total ($)</span>                    
                  </td>
                  <td className="text-end px-0">
                  <span className="fs-4 pe-3">= {total}</span>
                  </td>
                  
              </tr>        
              </tbody>
              </table>                                         
        </form>              
    )
}

const Salad = ({data, checkPrice, getForm}) => {

    let [total, updateTotal] = React.useState('00.00');  
    
    console.log('got data', data)

    let gardenSaladRef = React.useRef();
    let greekSaladRef = React.useRef();
    let antipastoRef = React.useRef();
    let tunaSaladRef = React.useRef();
         

    // React.useEffect(() => {        
    //     mozzarellaRef.current.checked = false;
    //     meatballsRef.current.checked = false;
    //     chickenRef.current.checked = false;
    // }, [data]);

    const getTotalPrice = React.useCallback(() => {
        let salad = [gardenSaladRef, greekSaladRef, antipastoRef, tunaSaladRef];
        let saladTotal = 0
        salad.forEach(pasta => {
            if (pasta.current.checked) {
                saladTotal += parseFloat(pasta.current.value)
            }
        })            
        
        if (saladTotal === 0) saladTotal = '00.00'
        updateTotal(toDecimalPlaces(String(saladTotal), 2).padStart(6));           
        checkPrice(saladTotal != 0)
        getForm(document.querySelector("#salad-form"))
    }, []);

    
    return (
        <form action="/shop/add/salad/" method="post" className='col-12 form-table-red py-3 px-2 mb-3' id="salad-form" data-food="Salad">   
        <CSRF />
        <table className="table" id="table-form">                                        
                                        <tbody>
            {data && data.map((salad, id) => {
                let refSalad, name, saladName;                
                console.log(salad.delicacy)
                if (/Garden/i.test(salad.delicacy)) {
                    refSalad = gardenSaladRef;
                    name = "garden"
                    saladName = "salad-Garden Salad"
                    // console.log('found moza', ref)
                } else if (/Greek/i.test(salad.delicacy)) {
                    refSalad = greekSaladRef;
                    name = "greek"
                    saladName = "salad-Greek Salad"
                    // console.log('found meat', ref)
                } else if (/Antipasto/i.test(salad.delicacy)) {
                    refSalad = antipastoRef;
                    name = "antipasto"
                    saladName = "salad-Antipasto"
                    // console.log('found chicken', ref)
                } else if (/Tuna/i.test(salad.delicacy)) {
                    refSalad = tunaSaladRef;
                    name = "tuna"
                    saladName = "salad-Salad w/ Tuna"
                    // console.log('found chicken', ref)
                }
            return (
                <tr key={id}>
                <td className="text-center">
                <input ref={refSalad} className="form-check-input" type="checkbox" name={saladName} id={name} onChange={() => getTotalPrice()} value={data && salad.fixed} />     
                </td>
                <td className="text-center px-0">
                <label className="form-check-label fs-5 salad-label" htmlFor={name}>{salad.delicacy}</label>                                                            
                </td>
                <td className="text-end">
                <p className="price fs-5 px-2">
                     {data && salad.fixed}
                </p>
                </td>                
            </tr>
            )
        })
        }                      
              <tr>
                  <td colSpan="2" className="text-center">
                  <span className="fs-4" style={{fontFamily: 'Arial'}}>Total ($)</span>                    
                  </td>
                  <td className="text-end px-0">
                  <span className="fs-4 pe-3">= {total}</span>
                  </td>                  
              </tr>         
              </tbody>
            </table>                   
        </form>              
    )
}

const Platter = ({data, checkPrice, getForm}) => {

    let [total, updateTotal] = React.useState('00.00');      
    

    let smallRef = React.useRef();
    let largeRef = React.useRef();
        

    // React.useEffect(() => {        
    //     smallRef.current.checked = false;
    //     largeRef.current.checked = false;
    // }, [data]);

    const getPrice = React.useCallback(() => {                        
        let platters = [smallRef, largeRef]

        let plattersTotal = 0
        platters.forEach(platter => {
            if (platter.current.checked) {
                plattersTotal += parseFloat(platter.current.value)
            }
        })            
        
        if (plattersTotal === 0) plattersTotal = '00.00'
        updateTotal(toDecimalPlaces(String(plattersTotal), 2).padStart(6));
               
        checkPrice(plattersTotal != 0)
        checkPrice((smallRef.current.checked || largeRef.current.checked))
        getForm(document.querySelector("#platter-form"))
    }, []);


    return (
        <form action="/shop/add/platter/" method="post" className='col-12 form-table-red py-3 px-2 mb-3' id="platter-form" data-food="Dinner Platter">  
        <CSRF /> 
        <h3 className="mb-4 text-center">{data.platter}</h3>      
        <input type='hidden' name="type" value={data.platter} />                          
        <table className="table" id="table-form">                                        
                                        <tbody>
            <tr>
                <td className="text-center">
                <input ref={smallRef} className="form-check-input" type="checkbox" name="small" id="small" onChange={() => getPrice()} value={data? data.small: '00.00'} /> 
                </td>
                
                <td className="text-center">
                <label className="form-check-label fs-4" htmlFor="small">Small</label>                                                            
                </td>
                <td className="text-end">
                <p className="price fs-4 px-1">
                     {data && data.small}
                </p>
                </td>
                
            </tr>
            <tr>
                <td className="text-center">
                <input ref={largeRef} className="form-check-input" type="checkbox" name="large" id="large" onChange={() => getPrice()} value={data? data.large: '00.00'} /> 
                </td>
                <td className="text-center">
                <label className="form-check-label fs-4" htmlFor="large">Large</label>                                                            
                </td>
                <td className="text-end">
                <p className="price fs-4 px-1">
                     {data && data.large}
                </p>    
                </td>
                
            </tr>
                                    
              <tr>
                  <td colSpan="2">
                  <span className="fs-4" style={{fontFamily: 'Arial'}}>Total ($)</span>                                  
                  </td>
                  <td className="text-end">
                  <span className="fs-4 px-1">= {total}</span>
                  </td>
                  
              </tr>     
              </tbody>                             
            </table>                       
        </form>              
    )
}