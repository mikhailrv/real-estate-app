import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import BASE_URL from '../config';

export default function AuthScreen({ navigation, route }) {
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const isLogin = route.name === 'Login';

  const handleAuth = async () => {
    setError(null);

    if (isLogin) {
      try {
        const response = await axios.post('http://BASE_URL/login/', {
          email,
          password,
        });
        console.log('Вход:', email, password);
        const token = response.data.access_token;
        await AsyncStorage.setItem('token', token);
        navigation.navigate('Home');
      } catch (err) {
        console.error('Ошибка при входе:', err);
        setError('Неверный email или пароль');
      } 

    } else {
      try {
        const response = await axios.post('http://192.168.42.245:8000/register/', {
          first_name,
          last_name,
          email,
          phone,
          password,
        });
        console.log('Регистрация:', response.data);
        navigation.navigate('Login');
      } catch (err) {
        console.error('Ошибка при регистрации:', err);
        setError('Проверьте данные, возможно email уже занят');
      }
    }
  };

  const handleNavigateToOtherScreen = () => {
    if (isLogin) {
      navigation.navigate('Register');
    } else {
      navigation.navigate('Login');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{isLogin ? 'Вход' : 'Регистрация'}</Text>

      {!isLogin && (
        <>
          <TextInput
            style={styles.input}
            placeholder="Имя"
            value={first_name}
            onChangeText={setFirstName}
          />
          <TextInput
            style={styles.input}
            placeholder="Фамилия"
            value={last_name}
            onChangeText={setLastName}
          />
          <TextInput
            style={styles.input}
            placeholder="Телефон"
            value={phone}
            onChangeText={setPhone}
            keyboardType="phone-pad"
          />
        </>
      )}

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <TextInput
        style={styles.input}
        placeholder="Пароль"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      
      <Button title={isLogin ? 'Войти' : 'Зарегистрироваться'} onPress={handleAuth} />

      <TouchableOpacity onPress={handleNavigateToOtherScreen} style={styles.register}>
        <Text style={styles.registerText}>
          {isLogin ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти'}
        </Text>
      </TouchableOpacity>

      {error && <Text style={{ color: 'red', textAlign: 'center' }}>{error}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
    backgroundColor: '#e0f7fa',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 16,
    textAlign: 'center',
    color: '#007aff',
  },
  input: {
    height: 48,
    borderWidth: 3,
    borderColor: '#007bff',
    paddingHorizontal: 12,
    marginBottom: 16,
    borderRadius: 16,
  },
  register: {
    marginTop: 16,
    alignItems: 'center',
  },
  registerText: {
    color: '#007aaf',
  },
});
