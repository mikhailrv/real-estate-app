import React, { useState, useEffect } from 'react'; 
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Image } from 'react-native';
import axios from 'axios';
import Icon from 'react-native-vector-icons/Ionicons';  
import AsyncStorage from '@react-native-async-storage/async-storage';
import BASE_URL from '../config';
import BottomNavigation from './components/bottomNavigation';
import ScreenTitle from './components/screenTitle';

export default function FavoritesScreen({ navigation }) {
  const [ads, setAds] = useState([]);

  useEffect(() => {
    const fetchAds = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get(BASE_URL+'/favorites/', {
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
      onPress={() => navigation.navigate('ListingDetails', { listingId: item.listing_id })}
    > 

      <Image source={{ uri: BASE_URL+`/${item.images[0]?.photo_url}` }} style={styles.cardImage} />

      <View style={styles.cardContent}> 

        <Text style={styles.price}>{Math.round(item.price)} руб.</Text>

        <Text style={styles.roomsAndArea}>{item.rooms} комнат, {item.area} м²</Text>

        <Text style={styles.address}>ул. {item.street}, {item.city}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <ScreenTitle title="Избранное" />
      <FlatList
        data={ads}
        keyExtractor={(item) => item.listing_id.toString()}
        renderItem={renderItem}
        numColumns={2}  
        contentContainerStyle={styles.listContainer}
      />
      <BottomNavigation /> 
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
});
