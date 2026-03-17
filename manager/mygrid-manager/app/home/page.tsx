export default function Home () {


  return (
    <div className="container">
      <h1 className="title">MyGrid Manager</h1>
      <div className="homeCategory">
        <h1 className="label">Sessions</h1>
        <button className="homeButton">Add results</button>
        <button className="homeButton" style={{ opacity: 0.5 }} disabled={true}>Update predictions</button>
        <h1 className="label">Notifications</h1>
        <button className="homeButton" style={{ opacity: 0.5 }} disabled={true}>Send notification</button>
        <button className="homeButton" style={{ opacity: 0.5 }} disabled={true}>Send mail</button>
      </div> 
    </div>
  )
}