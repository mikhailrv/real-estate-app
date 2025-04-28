// components/BottomNavigation.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { useNavigation } from '@react-navigation/native';

export default function BottomNavigation() {
  const navigation = useNavigation();

  return (
    <View style={styles.bottomButtons}>
      <TouchableOpacity onPress={() => navigation.navigate('Home')} style={styles.button}>
        <Icon name="home-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Главная</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Chats')} style={styles.button}>
        <Icon name="chatbubbles-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Сообщения</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Favorites')} style={styles.button}>
        <Icon name="heart-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Избранное</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Profile')} style={styles.button}>
        <Icon name="person-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Профиль</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
    bottomButtons: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        backgroundColor: '#fff',
        paddingVertical: 10,
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
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
