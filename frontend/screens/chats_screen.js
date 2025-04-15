import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import BASE_URL from '../config';

export default function ChatsScreen({ navigation }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get('http://BASE_URL/messages/chats/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setChats(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке чатов:', error);
      }
    };

    fetchChats();
  }, []);

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.chatCard}
      onPress={() => navigation.navigate('Messages', { chatId: item.chat_id })}
    >
      <View style={styles.chatInfo}>
        <Text style={styles.username}>{item.partner_name}</Text>
        <Text style={styles.lastMessage}>{item.last_message}</Text>
      </View>
      <Icon name="chevron-forward-outline" size={20} color="#aaa" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={chats}
        keyExtractor={(item) => item.chat_id.toString()}
        renderItem={renderItem}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9f9f9',
    paddingTop: 32,
  },
  listContainer: {
    padding: 10,
  },
  chatCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    elevation: 2,
  },
  chatInfo: {
    flex: 1,
  },
  username: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#007aff',
  },
  lastMessage: {
    fontSize: 14,
    color: '#555',
    marginTop: 4,
  },
});
