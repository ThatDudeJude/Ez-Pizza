const Order = () => {
    let [orderedItems, setOrderedItems] = React.useState(null)

    React.useEffect(async () => {
        const res = await fetch(`/order/view/show-orders/all/`, {
            method: 'GET'
        });
        const data = await res.json();
        console.log(data);
        setOrderedItems(data.length? data : null);
        let choiceOrder = document.querySelectorAll('.order-filter');
        choiceOrder.forEach((choice) => {
            choice.onchange = async () => {
                if (choice.checked) {
                    const res = await fetch(`/order/view/show-orders/${choice.value.toUpperCase()}/`, {
                        method: 'GET'
                    });
                    const data = await res.json();
                    console.log(data);
                    setOrderedItems(data.length? data : null);
                }                
            }
        })            
    }, [])
    

    return (
         <React.Fragment> 
             <h1 className="col-12 text-center">Ordered Items</h1>
                <h4 className="col-12 text-center">Filter by:</h4>
                    <div className='d-flex flex-wrap justify-content-around my-3'>
                        <div className="form-check form-check-inline py-2">
                            <label className="form-check-label" htmlFor="all">
                                <input className="form-check-input order-filter" type="radio" name="order-choice" id="all" value="All" defaultChecked /> All
                            </label>
                        </div>                            
                        <div className="form-check form-check-inline py-2">
                            <label className="form-check-label" htmlFor="placed">
                                <input className="form-check-input order-filter" type="radio" name="order-choice" id="placed" value="Placed" /> <i className="fas fa-shopping-bag fs-5"></i> Placed
                            </label>
                        </div>
                        <div className="form-check form-check-inline py-2">
                            <label className="form-check-label" htmlFor="cooking">
                                <input className="form-check-input order-filter" type="radio" name="order-choice" id="cooking" value="Cooking" /> <i className="fas fa-cheese fs-5"></i> Cooking
                            </label>
                        </div>
                        <div className="form-check form-check-inline py-2">
                            <label className="form-check-label" htmlFor="delivering">
                                <input className="form-check-input order-filter" type="radio" name="order-choice" id="delivering" value="Delivering" /> <i className="fas fa-shipping-fast fs-5"></i> Delivering
                            </label>
                        </div>
                        <div className="form-check form-check-inline py-2">
                            <label className="form-check-label" htmlFor="delivered">
                                <input className="form-check-input order-filter" type="radio" name="order-choice" id="delivered" value="Delivered" /> <i className="fas fa-pizza-slice fs-5"></i> Delivered
                            </label>
                        </div>
                    </div>
                    <table className="table table-striped table-hover col-12">
                        <thead>
                            <tr className="fs-5">
                                <th scope="Col">Food Item</th>
                                <th scope="Col">Choices</th>
                                <th scope="Col">Time Ordered</th>
                                <th scope="Col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orderedItems? orderedItems.map((item, id) => {
                                return (
                                <tr key={id}>                                                
                                    <td className="">{item.food_item}</td>
                                    <td className="">{item.choices}</td>
                                    <td className="">{item.human_time}</td>                                                
                                    <td className="">{item.status}</td>
                                </tr>                                                    
                                )
                            })
                            : 
                            <tr>
                                <td colSpan='4' className="text-center fs-3"> No Previously Ordered Items</td>
                            </tr>}
                        </tbody>                        
                    </table>                    

         </React.Fragment>           
    )
}

ReactDOM.render(<Order />, document.querySelector('#order-list'))