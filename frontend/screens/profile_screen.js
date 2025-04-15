import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, SafeAreaView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import Icon from 'react-native-vector-icons/Ionicons';
import BASE_URL from '../config';

export default function ProfileScreen({ navigation }) {
  const [user, setUser] = useState(null);
  const [editable, setEditable] = useState(false);
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: ''
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get('http://BASE_URL/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        });

        setUser(response.data);
        setForm({
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          email: response.data.email,
          phone: response.data.phone
        });

      } catch (error) {
        console.error('Ошибка при загрузке профиля:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleSave = async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await axios.put('http://192.168.1.129:8000/users/me', form, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
      setEditable(false);
      Alert.alert('Успешно', 'Данные обновлены!');
    } catch (error) {
      console.error('Ошибка при обновлении:', error);
      Alert.alert('Ошибка', 'Не удалось сохранить данные');
    }
  };

  return (
    <SafeAreaView style={styles.safeContainer}>
      <View style={styles.container}>
        <Text style={styles.title}>Профиль</Text>

        <TextInput
          style={styles.input}
          placeholder="Имя"
          value={form.first_name}
          onChangeText={(text) => setForm({ ...form, first_name: text })}
          editable={editable}
        />
        <TextInput
          style={styles.input}
          placeholder="Фамилия"
          value={form.last_name}
          onChangeText={(text) => setForm({ ...form, last_name: text })}
          editable={editable}
        />
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={form.email}
          onChangeText={(text) => setForm({ ...form, email: text })}
          editable={editable}
        />
        <TextInput
          style={styles.input}
          placeholder="Телефон"
          value={form.phone}
          onChangeText={(text) => setForm({ ...form, phone: text })}
          editable={editable}
        />

        <TouchableOpacity
          style={styles.editButton}
          onPress={editable ? handleSave : () => setEditable(true)}
        >
          <Text style={styles.editButtonText}>{editable ? 'Сохранить' : 'Редактировать'}</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.bottomButtons}>
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Home')}>
          <Icon name="home-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Главная</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button}>
          <Icon name="chatbubbles-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Сообщения</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Favorites')}> 
          <Icon name="heart-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Избранное</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Profile')}>
          <Icon name="person-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Профиль</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center'
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 10,
    marginBottom: 15,
    fontSize: 16,
  },
  editButton: {
    backgroundColor: '#007aff',
    paddingVertical: 12,
    borderRadius: 8,
    marginTop: 10,
  },
  editButtonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: 'bold',
  },
  bottomButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderTopWidth: 1,
    borderColor: '#eee',
    backgroundColor: '#fff',
  },
  button: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
    height: 60,
    backgroundColor: '#007aff',
    borderRadius: 15,
  },
  icon: {
    marginBottom: 5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 12,
  },
});
