
import React, { useEffect, useState } from 'react';
// import 'bootstrap/dist/css/bootstrap.css';
import { Card, CardGroup } from 'react-bootstrap';
import httpClient from "../httpClient";
import background from "../imgs/background2.webp";
import '../css/Dashboard.css';
// import Container from 'react-bootstrap/Container';
// import 'bootstrap/dist/css/bootstrap.min.css'

export default function Dashboard({ user }) {

  const [user_data, set_user_data] = useState({
    imageURL: user.imageURL,
    name: user.firstName,
    email: user.email,
    position: "faculty",
    department: "cse",
    total_casual_leaves: 0,
    taken_casual_leaves: 0,
    total_restricted_leaves: 0,
    taken_restricted_leaves: 0,
    total_earned_leaves: 0,
    taken_earned_leaves: 0,
    total_vacation_leaves: 0,
    taken_vacation_leaves: 0,
  });

  const [state, setState] = useState(null);

  const handleChange = (e) => {
    setState(e.target.files[0]);
  }

  const handleSubmit = async (e) => {

    e.preventDefault();
    const formData = new FormData();
    formData.append('file', state);
    fetch(
      '//localhost:5000/add_users',
      {
        method: 'POST',
        body: formData,
      }
    )
    alert("Users added successfully");

  }

  useEffect(() => {
    let isMounted = true;
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/dashboard");
        // console.log(resp.data);
        set_user_data(resp.data);
      }
      catch {
        // window.location.href = "/login"
      }
    })()
  }, []);

  return (
    // <div className="dashboard" style={{ height: "100vh", backgroundImage: `url(${background})`, backgroundPosition: "fixed", backgroundRepeat: "None", backgroundSize: "cover" }}>
    <div className="dashboard" style={{ margin: "0px", height: "100vh", backgroundColor: "aliceblue" }}>
      {/* <div className="Dashboard"> */}
      {/* <header className="jumbotron text-center"> */}
      <h2 className="heading">Dashboard</h2>
      <div className="heading-line"></div>

      <div className="container">
        <div className="main-body">

          <div className="row gutters-sm">

          {(user_data.position == "faculty" || user_data.position == "staff" || user_data.position == undefined || user_data.position == "") ? (
                        <a className="btn btn-info " style={{ "margin": "2px" }} href="displayLeaves">Applied Leaves</a>
                      ) : ('')}
            <div className="col-md-4 mb-3">
              <div className="card" style={{ "border": "2px solid grey" }}>
                <div className="card-body">
                  <div className="d-flex flex-column align-items-center text-center">
                    {(user.imageURL == "" || user.imageURL == undefined) ? (<img src={require("../imgs/loginIcon.png")} alt="Admin" className="rounded-circle" width="150" />)
                      : (<img src={user.imageURL} alt="Admin" className="rounded-circle" width="150" />)}

                    {/* <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="Admin" className="rounded-circle" width="150" /> */}
                    <div className="mt-3">
                      <h4>{user_data.name.toUpperCase()}</h4>
                      <p className="text-secondary mb-1">{user_data.position.toUpperCase()}</p>
                      <p className="text-secondary mb-1">{user_data.department.toUpperCase()}</p>
                      <p className="text-muted font-size-sm">{user_data.email}</p>
                      {/* <button className="btn btn-primary">Follow</button> */}
                      {(user_data.position == "faculty" || user_data.position == "staff" || user_data.position == undefined || user_data.position == "") ? (
                        <a href="leaveForm" style={{ margin: "10px" }}>
                          <button className="btn btn-outline-primary">Apply Leave</button>
                        </a>
                      ) : ('')}
                    </div>
                  </div>
                </div>
              </div>
              {/* <div className="card mt-3">
                <ul className="list-group list-group-flush">
                  <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                    <h6 className="mb-0"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-globe mr-2 icon-inline"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>Website</h6>
                    <span className="text-secondary">https://bootdey.com</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                    <h6 className="mb-0"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-github mr-2 icon-inline"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>Github</h6>
                    <span className="text-secondary">bootdey</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                    <h6 className="mb-0"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-twitter mr-2 icon-inline text-info"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>Twitter</h6>
                    <span className="text-secondary">@bootdey</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                    <h6 className="mb-0"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-instagram mr-2 icon-inline text-danger"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>Instagram</h6>
                    <span className="text-secondary">bootdey</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                    <h6 className="mb-0"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-facebook mr-2 icon-inline text-primary"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>Facebook</h6>
                    <span className="text-secondary">bootdey</span>
                  </li>
                </ul>
              </div> */}
            </div>
            <div className="col-md-8">
              <div className="card mb-3" style={{ "border": "2px solid grey" }}>
                <div className="card-body" >
                  <div className="row">
                    <div className="col-sm-6">
                      <h6 className="mb-0"><b>Leave Type</b></h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0"><b>Total</b></h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0"><b>Taken</b></h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0"><b>Remaining</b></h6>
                    </div>
                  </div>
                  <hr />

                  <div className="row">
                    <div className="col-sm-6">
                      <h6 className="mb-0">Casual Leaves</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_casual_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.taken_casual_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_casual_leaves - user_data.taken_casual_leaves}</h6>
                    </div>

                  </div>
                  <hr />
                  <div className="row">
                    <div className="col-sm-6">
                      <h6 className="mb-0">Restricted Leaves</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_restricted_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.taken_restricted_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_restricted_leaves - user_data.taken_restricted_leaves}</h6>
                    </div>
                  </div>
                  <hr />
                  <div className="row">
                    <div className="col-sm-6">
                      <h6 className="mb-0">Earned Leaves</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_earned_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.taken_earned_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_earned_leaves - user_data.taken_earned_leaves}</h6>
                    </div>
                  </div>
                  <hr />
                  <div className="row">
                    <div className="col-sm-6">
                      <h6 className="mb-0">Vacation Leaves</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_vacation_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.taken_vacation_leaves}</h6>
                    </div>
                    <div className="col-sm-2">
                      <h6 className="mb-0">{user_data.total_vacation_leaves - user_data.taken_vacation_leaves}</h6>
                    </div>
                  </div>
                  <hr />

                  {/* <div className="row">
                    <div className="col-sm-3">
                      <h6 className="mb-0">Address</h6>
                    </div>
                    <div className="col-sm-9 text-secondary">
                      Bay Area, San Francisco, CA
                    </div>
                  </div> */}
                  {/* <hr /> */}
                  <div className="row">
                    <div className="col-sm-12" >
                      {(user_data.position == "faculty" || user_data.position == "staff" || user_data.position == undefined || user_data.position == "") ? (
                        <a className="btn btn-info " style={{ "margin": "2px" }} href="displayLeaves">Applied Leaves</a>
                      ) : (
                        <div>
                          {/* <a className="btn btn-info " style={{ "margin": "2px" }} href="displayLeaves">Applied Leaves</a> */}
                          <a className="btn btn-info " style={{ "margin": "2px" }} href="checkLeaves">Check Leaves</a>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {(user_data.position == "admin" || user_data.position == "admin") ? (
                <div className="card mb-3" style={{ "border": "2px solid grey" }}>
                  <div className="card-body" >
                    <h2>Add Users</h2>
                    <div className="row">
                      <div className="col-sm-12" style={{ "padding": "0px", "margin": "0px" }}>
                        <form onSubmit={handleSubmit}>
                          <input onChange={handleChange} type="file" />
                          <input type="submit" value="Upload" />
                        </form>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                ''
              )}


              {/* <div className="row gutters-sm">
                <div className="col-sm-6 mb-3">
                  <div className="card h-100">
                    <div className="card-body">
                      <h6 className="d-flex align-items-center mb-3"><i className="material-icons text-info mr-2">assignment</i>Project Status</h6>
                      <small>Web Design</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "80%"}} aria-valuenow="80" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>Website Markup</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "72%"}} aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>One Page</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "89%"}} aria-valuenow="89" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>Mobile Template</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "55%"}} aria-valuenow="55" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>Backend API</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "66%"}} aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="col-sm-6 mb-3">
                  <div className="card h-100">
                    <div className="card-body">
                      <h6 className="d-flex align-items-center mb-3"><i className="material-icons text-info mr-2">assignment</i>Project Status</h6>
                      <small>Web Design</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "80%"}} aria-valuenow="80" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>Website Markup</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "72%"}} aria-valuenow="72" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>One Page</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "89%"}} aria-valuenow="89" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>Mobile Template</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "55%"}} aria-valuenow="55" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <small>Backend API</small>
                      <div className="progress mb-3" style={{"height": "5px"}}>
                        <div className="progress-bar bg-primary" role="progressbar" style={{"width": "66%"}} aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div> */}



            </div>
          </div>

        </div>
      </div>

    </div>
  );
}

