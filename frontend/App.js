import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native'; 
import { createStackNavigator } from '@react-navigation/stack'; 
import AuthScreen from './screens/auth_screen'; 
import HomeScreen from './screens/home_screen'; 
import ProfileScreen from './screens/profile_screen'; 
import FavoritesScreen from './screens/favorites_screen'; 
import 'react-native-gesture-handler';
import ChatsScreen from './screens/chats_screen'; 
import ListingDetailsScreen from './screens/listing_details_screen';
import MessagesScreen from './screens/messages_screen';
import SearchScreen from './screens/search_screen';
import { SafeAreaView } from 'react-native-safe-area-context';

const Stack = createStackNavigator(); 

export default function App() {
  return (
    <NavigationContainer>
      <SafeAreaView style={{ flex: 1 }}>
        <Stack.Navigator>
          <Stack.Screen name="Login" component={AuthScreen} />
          <Stack.Screen name="Register" component={AuthScreen} />
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Profile" component={ProfileScreen} />
          <Stack.Screen name="Favorites" component={FavoritesScreen} />
          <Stack.Screen name="Chats" component={ChatsScreen} />
          <Stack.Screen name="ListingDetails" component={ListingDetailsScreen} />
          <Stack.Screen name="Messages" component={MessagesScreen} />
          <Stack.Screen name="Search" component={SearchScreen} />
        </Stack.Navigator>
      </SafeAreaView>
    </NavigationContainer>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});



