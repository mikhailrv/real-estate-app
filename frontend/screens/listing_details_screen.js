import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Image, Dimensions, ScrollView } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Carousel from 'react-native-reanimated-carousel';
import BASE_URL from '../config';

const { width: screenWidth } = Dimensions.get('window');

export default function ListingDetailsScreen({ route }) {
  const { listingId } = route.params;
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeSlide, setActiveSlide] = useState(0);

  useEffect(() => {
    const fetchListing = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get(`${BASE_URL}/ads/${listingId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setListing(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке объявления:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchListing();
  }, [listingId]);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007bff" />
      </View>
    );
  }

  if (!listing) {
    return (
      <View style={styles.centered}>
        <Text>Объявление не найдено</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {listing.images.length > 0 && (
        <>
          {listing.images.length > 1 ? (
            <>
              <Carousel
                width={screenWidth}
                height={350} 
                data={listing.images}
                scrollAnimationDuration={500}
                onSnapToItem={(index) => setActiveSlide(index)}
                renderItem={({ item }) => (
                  <Image source={{ uri: BASE_URL + `/${item.photo_url}` }} style={styles.image} />
                )}
                loop
              />
              <View style={styles.pagination}>
                {listing.images.map((_, index) => (
                  <View
                    key={index}
                    style={[
                      styles.dot,
                      index === activeSlide ? styles.activeDot : null,
                    ]}
                  />
                ))}
              </View>
            </>
          ) : (
            <Image
              source={{ uri: BASE_URL + `/${listing.images[0].photo_url}` }}
              style={styles.image}
            />
          )}
        </>
      )}


      <View style={styles.infoContainer}>
        <Text style={styles.price}>{listing.price} ₽</Text>
        <Text style={styles.type}>{listing.property_type.name}</Text>

        <Text style={styles.label}>Описание:</Text>
        <Text style={styles.text}>{listing.description}</Text>

        <Text style={styles.label}>Адрес:</Text>
        <Text style={styles.text}>
          г. {listing.city}, ул. {listing.street}, д. {listing.house_number}
          {listing.apartment_number ? `, кв. ${listing.apartment_number}` : ''}
        </Text>

        <Text style={styles.label}>
          Площадь: <Text style={styles.text}>{listing.area} м²</Text>
        </Text>
        <Text style={styles.label}>
          Комнат: <Text style={styles.text}>{listing.rooms}</Text>
        </Text>
        <Text style={styles.label}>
          Санузлов: <Text style={styles.text}>{listing.bathrooms}</Text>
        </Text>

        <Text style={styles.label}>Категории:</Text>
        <View style={styles.categories}>
          {listing.categories.map((cat) => (
            <View key={cat.category_id} style={styles.categoryTag}>
              <Text style={styles.categoryText}>{cat.name}</Text>
            </View>
          ))}
        </View>

        <Text style={styles.date}>
          Добавлено: {new Date(listing.created_at).toLocaleDateString()}
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: screenWidth,
    height: 350,
  },
  infoContainer: {
    padding: 20,
  },
  price: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#007bff',
  },
  type: {
    fontSize: 18,
    marginTop: 5,
    color: '#555',
  },
  label: {
    marginTop: 15,
    fontWeight: 'bold',
    fontSize: 16,
    color: '#000',
  },
  text: {
    fontSize: 16,
    color: '#333',
    marginTop: 4,
  },
  categories: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 5,
  },
    categoryTag: {
      backgroundColor: '#e0e0e0',
      borderRadius: 12,
      paddingHorizontal: 10,
      paddingVertical: 5,
      marginRight: 8,
      marginBottom: 5,
    },
  categoryText: {
    fontSize: 14,
    color: '#000',
  },
  date: {
    marginTop: 20,
    fontSize: 12,
    color: '#888',
  },
  pagination: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 10,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#ccc',
    marginHorizontal: 4,
  },
  activeDot: {
    backgroundColor: '#007bff',
    width: 10,
    height: 10,
  },
});
