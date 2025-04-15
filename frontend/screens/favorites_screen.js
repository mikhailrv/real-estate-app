import React, { useState, useEffect } from 'react'; 
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Image } from 'react-native';
import axios from 'axios';
import Icon from 'react-native-vector-icons/Ionicons';  
import AsyncStorage from '@react-native-async-storage/async-storage';
import BASE_URL from '../config';

export default function FavoritesScreen({ navigation }) {
  const [ads, setAds] = useState([]);

  useEffect(() => {
    const fetchAds = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get('http://BASE_URL/favorites', {
            headers: { Authorization: `Bearer ${token}` }
          })
        setAds(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке объявлений", error);
      }
    };

    fetchAds();
  }, []);

  const renderItem = ({ item }) => (
    <TouchableOpacity 
      style={styles.card} 
      onPress={() => navigation.navigate('AdDetail', { listingId: item.listing_id })} 
    > 

      <Image source={{ uri: `http://192.168.42.245:8000/${item.images[0]?.photo_url}` }} style={styles.cardImage} />

      <View style={styles.cardContent}> 

        <Text style={styles.price}>{Math.round(item.price)} руб.</Text>

        <Text style={styles.roomsAndArea}>{item.rooms} комнат, {item.area} м²</Text>

        <Text style={styles.address}>ул. {item.street}, {item.city}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>

      <FlatList
        data={ads}
        keyExtractor={(item) => item.listing_id.toString()}
        renderItem={renderItem}
        numColumns={2}  
        contentContainerStyle={styles.listContainer}
      />

      <View style={styles.bottomButtons}>
        
        <TouchableOpacity onPress={() => navigation.navigate('Home')} style={styles.button}>
          <Icon name="home-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Главная</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button}>
          <Icon name="chatbubbles-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Сообщения</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button}>
          <Icon name="heart-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Избранное</Text>
        </TouchableOpacity>
        
        <TouchableOpacity onPress={() => navigation.navigate('Profile')} style={styles.button} >
          <Icon name="person-outline" size={30} color="#fff" style={styles.icon} />
          <Text style={styles.buttonText}>Профиль</Text>
          
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 32,
    backgroundColor: '#f9f9f9',
  },
  searchButton: {
    backgroundColor: '#007aff',
    paddingVertical: 10,
    paddingHorizontal: 120,
    borderRadius: 5,
    alignSelf: 'center',
    marginBottom: 10,
  },
  searchButtonText: {
    color: '#fff',
    fontSize: 18,
  },
  listContainer: {
    paddingBottom: 40,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    margin: 10,
    flex: 1,
    height: 250,  
  },
  cardImage: {
    width: '100%',
    height: 120,  
    borderTopLeftRadius: 10,
    borderTopRightRadius: 10,
  },
  cardContent: {
    padding: 10,
    justifyContent: 'center',
    flex: 1,
  },
  price: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#007aff',
  },
  roomsAndArea: {
    fontSize: 14,
    color: '#555',
  },
  address: {
    fontSize: 12,
    color: '#888',
  },
  bottomButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
    marginTop: 10,
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
