import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import axios from 'axios';
import BASE_URL from '../config';

export default function SearchScreen({ navigation }) {
  const [city, setCity] = useState('');
  const [priceMin, setPriceMin] = useState('');
  const [priceMax, setPriceMax] = useState('');
  const [rooms, setRooms] = useState('');

  const handleSearch = async () => {
    try {
      const params = {};

      if (city) params.city = city;
      if (priceMin) params.price_min = priceMin;
      if (priceMax) params.price_max = priceMax;
      if (rooms) params.rooms = rooms.split(',').map(r => r.trim()); 

      const response = await axios.get(BASE_URL + '/ads/', { params });
      const results = response.data;

      navigation.navigate('SearchResults', { results });
    } catch (error) {
      console.error('Ошибка поиска', error);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.label}>Город:</Text>
      <TextInput style={styles.input} value={city} onChangeText={setCity} placeholder="Например, Москва" />

      <Text style={styles.label}>Цена от:</Text>
      <TextInput style={styles.input} value={priceMin} onChangeText={setPriceMin} keyboardType="numeric" />

      <Text style={styles.label}>Цена до:</Text>
      <TextInput style={styles.input} value={priceMax} onChangeText={setPriceMax} keyboardType="numeric" />

      <Text style={styles.label}>Количество комнат (через запятую):</Text>
      <TextInput style={styles.input} value={rooms} onChangeText={setRooms} placeholder="1,2,3" keyboardType="numeric" />

      <TouchableOpacity style={styles.button} onPress={handleSearch}>
        <Text style={styles.buttonText}>Искать</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  label: {
    marginTop: 10,
    fontSize: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    borderRadius: 5,
    marginTop: 5,
  },
  button: {
    backgroundColor: '#007aff',
    marginTop: 20,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
});
