import { useEffect } from 'react';
import { registerUser } from './services/api';

function App() {
    useEffect(() => {
        registerUser({ username: 'frontend_test', password: '123456' })
            .then(res => console.log(res.data))
            .catch(err => console.error(err));
    }, []);

    return <h1>Testing Backend Connection</h1>;
}

export default App;
