import ReactDOM from 'react-dom/client'

const WelcomeText = () => {
  const target = 'world'
  return <h1>Hello, {target}!</h1>
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <div>
    <WelcomeText />
  </div>
)