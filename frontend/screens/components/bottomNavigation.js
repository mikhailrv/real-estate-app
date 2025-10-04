import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';  
import { useNavigation } from '@react-navigation/native';

export default function BottomNavigation() {
  const navigation = useNavigation();

  return (
    <View style={styles.bottomButtons}>
      <TouchableOpacity onPress={() => navigation.navigate('Home')} style={styles.button}>
        <Ionicons name="home-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Главная</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Chats')} style={styles.button}>
        <Ionicons name="chatbubbles-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Сообщения</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Favorites')} style={styles.button}>
        <Ionicons name="heart-outline" size={30} color="#fff" style={styles.icon} />
        <Text style={styles.buttonText}>Избранное</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Profile')} style={styles.button}>
        <Ionicons name="person-outline" size={30} color="#fff" style={styles.icon} />
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
