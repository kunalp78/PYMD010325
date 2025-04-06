"""
Movie Booking System
Features:
1.	User Registration and Login:
	Users can register and log in to book tickets.
	Credentials are stored securely in memory.
2.	Movie and Show Management:
	Admin can add movies and show timings.
	Users can view available movies and their timings.
3.	Seat Booking:
	Users can select a movie, showtime, and book seats.
	Seats are dynamically updated based on availability.
4.	Booking History:
	Users can view their past bookings.
"""
import json
import datetime


class User:
    """
    User: 
        Handles user details, login, and registration.
    
    User sample:
    {
        "user_name": {
            "name": ...,
            "phone": ...,
            ...
        }
    }

    """
    def __init__(self, username, name, password, phoneno):
        self.__username = username
        self.__name = name
        self.__password = password
        self.__phone = phoneno
        self.__login_log = []
        self.__booking = []
    
    @staticmethod
    def save_user_to_json(username, name, password, phoneno, login_log=[], booking=[]):
        user = {
            username: {
                "name": name,
                "password": password,
                "phone_number": phoneno,
                "login_log": login_log,
                "booking": booking
            }
        }
        try:
            fp = open("users.json", "r+")
            content = json.load(fp)
        except FileNotFoundError:
            fp = open("users.json", "w+")
            content = {}
        except json.JSONDecodeError:
            content = {}

        if username not in content:
            user[username]["login_log"].append(str(datetime.datetime.now()))
            content.update(user)
            fp.seek(0)
            fp.truncate()
            json.dump(content, fp, indent=2)
            fp.close()
        else:
            fp.close()
            raise Exception("User already registerd")
    
    @staticmethod
    def get_from_json(file_pointer):
        try:
            content = json.load(file_pointer)
        except json.JSONDecodeError:
            print("This file in incompatible with JSON!")
            return {}
        return content
    
    @classmethod
    def register(cls):
        user = input("Enter your name: ")
        password = input("Enter your password: ")
        phno = input("Enter your phone number: ")
        username = user[0].lower() + phno[1:4]
        try:
            user_obj  = User(username, user, password, phno)
            cls.save_user_to_json(user_obj.__username,
                                  user_obj.__name,
                                  password,
                                  user_obj.__phone)
            print(f"Your username is: {username}")
            print("You have been registered sucessfully!")
            return username
        except Exception as e:
            import traceback
            print(traceback.print_exc())
            print(e)

    @staticmethod
    def login():
        fp = open("users.json", "r+")
        users = User.get_from_json(fp)
        username = input("Enter your Username: ")
        password = input("Enter your password: ")
        if username in users:
            if users[username]["password"] == password:
                users[username]["login_log"].append(str(datetime.datetime.now()))
                fp.seek(0)
                fp.truncate()
                json.dump(users, fp, indent=2)
                fp.close()
                print("Login sucessfull...\nWelcome to the Dashboard!!")
                return username
            else:
                print("Incorrect Password!!")
                # make a mechanism to enable user to reset password
                return
        else:
            print("Incorrect username!")
            forgot_username = input("Did you forget username [Y/n]: ")
            if forgot_username.lower() == "y":
                forgot_username = input("Do you want to login by providing your name and phno. [Y/n]")
                if forgot_username.lower() == "y":
                    name = input("Enter your name: ")
                    phno = input("Enter your phone number: ")
                    password = input("Enter your password: ")
                    username = name[0].lower() + phno[1:4]
                    if username in users:
                        if users[username]["password"] == password:
                            users[username]["login_log"].append(str(datetime.datetime.now()))
                            fp.seek(0)
                            fp.truncate()
                            json.dump(users, fp, indent=2)
                            fp.close()
                            print("Login sucessfull...\nWelcome to the Dashboard!!")
                            return username
                        else:
                            print("Incorrect Password!!")
                            # make a mechanism to enable user to reset password
                            return
                    else:
                        print("User doesnot exists.\nPlease register!!")
                        return


class Movie:
    """
    Movie:
        Stores information about movies, showtimes, and available seats.
    """
    @classmethod
    def create_movie_info(cls, title, showtime, total_seats):
        if cls.__name__ != "Admin":
            raise Exception("No Admin Privilage to Movies")
        movie_dict = {
            "title": title,
            "showtime": showtime,
            "total_seats": int(total_seats),
            "available_seats": int(total_seats)
        }
        try:
            fp = open("movies.json",  "r+")
            content = json.load(fp)
        except FileNotFoundError:
            fp = open("movies.json", "w+")
            content = []
        except json.JSONDecodeError:
            content = []
        if movie_dict not in content:
            content.append(movie_dict)
            fp.seek(0)
            fp.truncate()
            json.dump(content, fp, indent=2)
        else:
            print("Movie already exists!")
    
    @staticmethod
    def find_movie(title):
        fp = open("movies.json", "r")
        content = json.load(fp)
        fp.close()
        for i in range(len(content)):
            if title == content[i]["title"]:
                return content[i]
        print("Movie not found!!")

class Booking:
    """
    Booking:
        Manages booking information, such as movie, user, and seat details.
    """
    @staticmethod
    def save_booking_info(username, movie_name, seats_booked):
        booking = {
            "username": username,
            "movie_name": movie_name,
            "seats_booked": seats_booked,
            "booking_time": str(datetime.datetime.now())
        }
        try:
            movie_p = open("booking.json", "r+")
            movie_content = json.load(movie_p)
        except FileNotFoundError:
            movie_p = open("booking.json", "w+")
            movie_content = []

        movie_content.append(booking)
        movie_p.seek(0)
        movie_p.truncate()
        json.dump(movie_content, movie_p, indent=2)
        movie_p.close()

        try:
            user_p = open("users.json", "r+")
            user_content = json.load(user_p)
        except (FileNotFoundError, json.JSONDecodeError):
            print("There is no user available to book the movie!!")
            return

        user_content[username]["booking"].append(booking)
        user_p.seek(0)
        user_p.truncate()
        json.dump(user_content, user_p, indent=2)
        user_p.close()
        print("Booking Successful!!")


class Admin(Movie):
    """
    Admin:
        Manages movie and showtime additions.
    """
    key = 1033923070941875036
    def __init__(self, admin_user, admin_password):
        self.admin_user = admin_user
        self.admin_password = hash(admin_password)
        # try:
        #     fp = open("admin.json", "r+")
        #     content = json.load(fp)
        # except FileNotFoundError:
        #     fp = open("admin.json", "w+")
        #     content = []
        # except json.JSONDecodeError:
        #     content = []
        # if self.__dict__ not in content:
        #     content.append(self.__dict__)
        # fp.seek(0)
        # fp.truncate()
        # json.dump(content, fp, indent=2)

    # def __new__(cls, *args, **kwargs):
    #     try:
    #         fp = open("admin.json", "r+")
    #         content = json.load(fp)
    #         fp.close()
    #     except json.JSONDecodeError:
    #         content = []
    #     except FileNotFoundError:
    #         print("No admins available!!")
    #         fp = open("admin.json", "w+")
    #         fp.close()
    #         content = []
    #     if content:
    #         if input("Do you want to create a new admin[Y/n]: ").lower() == "y":
    #             if input("Enter the key") != cls.key:
    #                 raise "Not Authorised to create Admins"
    #             else:
    #                 return super().__new__(cls, *args, **kwargs)
    
    @classmethod
    def create_movie(cls):
        title = input("Enter the movie title: ")
        showtime = input("Enter the show time: ")
        total_seats = input("Enter the total number of seats: ")
        cls.create_movie_info(title, showtime, total_seats)
        print("A new movie is added!!")

def main():
    admin_name = input("Enter the username of admin: ")
    admin_password = int(input("Enter the password of admin: "))
    admin = Admin(admin_name, admin_password)

    fp = open("admin.json")
    content = json.load(fp)
    fp.close()
    flag = 0
    for i in range(len(content)):
        if content[i]["admin_user"] == admin_name:
            print(admin_password, content[i]["admin_password"])
            if content[i]["admin_password"] == hash(admin_password):
                flag += 1
                print("Login successfull!")
                print("!!Movie Booking System Menu!!")
            else:
                print("Incorrect admin password!!")
                return
    while flag:
        try:
            print("\n1) Register\n2) Login\n3) Admin Login\n4) Logout")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                username = User.register()
                # HW: Impliment login here as well based on the username you have
            elif choice == 2:
                username = User.login()
                if username:
                    print("Movie Booking menu!!")
                    while True:
                        print("\n1) View Movie\n2) Book Movie\n3) View Booking\n4) Logout")
                        user_choice = int(input("Enter your choice: "))
                        if user_choice == 1:
                            movie_p = open("movies.json", "r")
                            movie_content = json.load(movie_p)
                            movie_p.close()
                            for i in range(len(movie_content)):
                                print(movie_content[i]) # create a method to beutify movies
                        elif user_choice == 2:
                            movie_name = input("Enter the name of the movie: ")
                            movie = Movie.find_movie(movie_name)
                            if movie:
                                seats = input("Enter the number of seats: ")
                                movie_fp = open("movies.json", "r+")
                                movie_content = json.load(movie_fp)
                                booking_flag = 0
                                for mv in range(len(movie_content)): # here below I used mv but you should use movie_content
                                    if movie_content[i]["title"] == movie_name:
                                        if movie_content[i]["available_seats"] >= int(seats):
                                            movie_content[i]["available_seats"] -= int(seats)
                                            Booking.save_booking_info(
                                                                    username,
                                                                    movie_name,
                                                                    seats
                                                                    )
                                            booking_flag+=1
                                            break
                                        else:
                                            print("Not enough seats")
                                    else:
                                        print("Housefull!")
                                if booking_flag > 0:
                                    movie_fp.seek(0)
                                    movie_fp.truncate()
                                    json.dump(movie_content, movie_fp, indent=2)
                                    movie_fp.close()
                            else:
                                print("Movie you asked doesnot exist!!")
                        elif user_choice == 3:
                            users = open("users.json")
                            content = json.load(users)
                            print(content[username]["booking"])
                            users.close()
                            # Impliment this in a decorative fashion
                        elif user_choice == 4:
                            print("Logging Out ...")
                            break
                        else:
                            print("Incorrect choice.")
                else:
                    print("Enter the credentials again!!")
            elif choice == 3:
                print("Welcome to Admin Dashboard:")
                print("\n1) Add Movie\n2) View Movie\n3) Logout")
                amdin_choice = int(input("Enter your choice [1-3]: "))
                if amdin_choice == 1:
                    Admin.create_movie()
                elif amdin_choice == 2:
                    fp = open("movies.json")
                    content = json.load(fp)
                    for i in range(len(content)):
                        print(content[i])
                elif amdin_choice == 3:
                    print("Logging out of Admin dashboard!!")
                    break
                else:
                    print("Emter valid choice!")
            elif choice == 4:
                print("Hope you enjoyed our company!!")
                print("Logging out ...")
                break
            else:
                print("Enter the choices between [1-4]")
        except Exception as e:
            import traceback
            print(traceback.print_exc())
            print("Your Choice should be an Number!!")

    if flag == 0:
        print("Incorrect admin password!!")
main()
