import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Keyboard } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import BASE_URL from '../config';
import BottomNavigation from './components/bottomNavigation';
import ScreenTitle from './components/screenTitle';

export default function ChatsScreen({ navigation }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await axios.get(BASE_URL + '/messages/chats', {
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
        <View style={styles.chatHeader}>
          <Text style={styles.username}>
            {item.companion.first_name + ' ' + item.companion.last_name}
          </Text>
          <Text style={styles.time}>
            {new Date(item.last_message.sent_at).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </Text>
        </View>
  
        <View style={styles.messageRow}>
          <Text
            style={[
              styles.lastMessage,
              item.unread_count > 0 && styles.unreadMessage,
            ]}
            numberOfLines={1}
          >
            {item.last_message.message}
          </Text>
  
          {item.unread_count > 0 && (
            <View style={styles.unreadBadge}>
              <Text style={styles.unreadCount}>{item.unread_count}</Text>
            </View>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
  
  
  return (
    <View style={styles.container}>
      <ScreenTitle title="Сообщения" />
      <FlatList
        data={chats}
        keyExtractor={(item) => item.chat_id.toString()}
        renderItem={renderItem}
        contentContainerStyle={styles.listContainer}
      />

      <BottomNavigation />
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
    paddingBottom: 70,
  },
  chatCard: {
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    paddingVertical: 24,
    paddingHorizontal: 20,
  },
  chatInfo: {
    flex: 1,
  },
  chatHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 2,
  },
  username: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#000',
  },
  time: {
    fontSize: 12,
    color: '#888',
  },
  lastMessage: {
    fontSize: 14,
    color: '#555',
    marginTop: 10,
  },
  timeContainer: {
    alignItems: 'flex-end',
  },
  unreadBadge: {
    backgroundColor: '#007bff',
    borderRadius: 10,
    paddingHorizontal: 8,
    paddingVertical: 3,
    marginTop: 1,
    alignSelf: 'flex-end',
    marginLeft: 260,
  },
  unreadCount: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  unreadMessage: {
    fontWeight: 'bold',
    color: '#000',
  },
  messageRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
});
