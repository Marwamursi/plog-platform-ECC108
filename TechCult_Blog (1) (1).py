import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTextEdit, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TechCult Blog")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0.193, x2:0.829, y2:0.301136, stop:0 rgba(66, 183, 255, 255), stop:1 rgba(232, 43, 255, 255));
            border-radius: 25px;
            font-size: 16px;  /* Set default font size */
        """)

        self.logged_in = False
        self.current_user = None
        self.posts = []
        self.user_email = ""
        self.user_bio = ""

        self.create_widgets()

    def create_widgets(self):
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("""
            background-color: black;
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
        """)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setStyleSheet("""
            background-color: black;
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
        """)
        self.logout_button.hide()

        self.profile_button = QPushButton("Profile Page")
        self.profile_button.clicked.connect(self.show_profile)
        self.profile_button.setStyleSheet("""
            background-color: black;
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
        """)
        self.profile_button.hide()

        self.posts_layout = QVBoxLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter username")
        self.username_edit.setStyleSheet("font-size: 16px;")  # Set font size for QLineEdit

        layout = QVBoxLayout()
        layout.addWidget(self.username_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.profile_button)

        self.posts_scroll = QtWidgets.QScrollArea()
        self.posts_scroll.setWidgetResizable(True)
        self.posts_widget = QtWidgets.QWidget()
        self.posts_widget.setLayout(self.posts_layout)
        self.posts_scroll.setWidget(self.posts_widget)
        
        layout.addWidget(self.posts_scroll)

        self.create_post_button = QPushButton("Create Post")
        self.create_post_button.clicked.connect(self.create_post)
        self.create_post_button.setStyleSheet("""
            background-color: black;
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
        """)
        
        layout.addWidget(self.create_post_button)

        layout.setContentsMargins(25, 25, 25, 25)
        self.setLayout(layout)

    def login(self):
        username = self.username_edit.text().strip()
        if not username:
            QMessageBox.information(self, "Login", "Please enter username.")
            return

        if not self.logged_in:
            self.logged_in = True
            self.current_user = username
            QMessageBox.information(self, "Login", f"Welcome, {username}!")
            self.update_posts()
            self.login_button.hide()
            self.logout_button.show()
            self.profile_button.show()
        else:
            QMessageBox.information(self, "Login", "You are already logged in!")

    def logout(self):
        self.logged_in = False
        self.current_user = None
        self.login_button.show()
        self.logout_button.hide()
        self.profile_button.hide()

    def show_profile(self):
        profile_dialog = ProfileDialog(self)
        profile_dialog.exec_()

    def create_post(self):
        if not self.logged_in:
            QMessageBox.information(self, "Create Post", "You need to log in first!")
            return

        title, ok1 = QtWidgets.QInputDialog.getText(self, "Create Post", "Enter post title:")
        content, ok2 = QtWidgets.QInputDialog.getText(self, "Create Post", "Enter post content:")
        topic, ok3 = QtWidgets.QInputDialog.getText(self, "Create Post", "Enter post topic:")

        if ok1 and ok2 and ok3:
            post = {
                "title": title,
                "content": content,
                "topic": topic,  # Add the topic to the post dictionary
                "author": self.current_user,
                "likes": set(),  # Initialize likes as a set to store unique user IDs
                "dislikes": set(),  # Initialize dislikes as a set to store unique user IDs
                "comments": [],
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.posts.append(post)
            self.update_posts()

    def delete_post(self, button):
        post_index = self.posts_layout.indexOf(button.parentWidget())
        if post_index != -1:
            button.parentWidget().deleteLater()
            self.posts.pop(post_index)

    def add_comment(self, button):
        post_index = self.posts_layout.indexOf(button.parentWidget())
        if post_index != -1:
            comment, ok = QtWidgets.QInputDialog.getText(self, "Add Comment", "Enter your comment:")
            if ok:
                self.posts[post_index]["comments"].append({"author": self.current_user, "content": comment})
                self.update_posts()

    def like_post(self, button):
        post_index = self.posts_layout.indexOf(button.parentWidget())
        if post_index != -1:
            post = self.posts[post_index]
            if self.current_user not in post["likes"]:
                post["likes"].add(self.current_user)
                if self.current_user in post["dislikes"]:
                    post["dislikes"].remove(self.current_user)
                self.update_posts()
            else:
                QMessageBox.information(self, "Like", "You have already liked this post.")

    def dislike_post(self, button):
        post_index = self.posts_layout.indexOf(button.parentWidget())
        if post_index != -1:
            post = self.posts[post_index]
            if self.current_user not in post["dislikes"]:
                post["dislikes"].add(self.current_user)
                if self.current_user in post["likes"]:
                    post["likes"].remove(self.current_user)
                self.update_posts()
            else:
                QMessageBox.information(self, "Dislike", "You have already disliked this post.")

    def update_posts(self):
        # Clear existing posts
        for i in reversed(range(self.posts_layout.count())):
            self.posts_layout.itemAt(i).widget().deleteLater()

        # Add new posts
        for post in self.posts:
            post_widget = QtWidgets.QWidget()
            layout = QVBoxLayout(post_widget)
            
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                background-color: black;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
            """)
            delete_button.clicked.connect(lambda _, b=delete_button: self.delete_post(b))

            comment_button = QPushButton("Add Comment")
            comment_button.setStyleSheet("""
                background-color: black;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
            """)
            comment_button.clicked.connect(lambda _, b=comment_button: self.add_comment(b))

            like_button = QPushButton("Like")
            like_button.setStyleSheet("""
                background-color: black;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
            """)
            like_button.clicked.connect(lambda _, b=like_button: self.like_post(b))

            dislike_button = QPushButton("Dislike")
            dislike_button.setStyleSheet("""
                background-color: black;
                color: white;
                border-radius: 15px;
                padding: 5px 10px;
            """)
            dislike_button.clicked.connect(lambda _, b=dislike_button: self.dislike_post(b))

            layout.addWidget(QtWidgets.QLabel(f"Title: {post['title']}"))
            layout.addWidget(QtWidgets.QLabel(f"Author: {post['author']}"))
            layout.addWidget(QtWidgets.QLabel(f"Topic: {post['topic']}"))  # Display the topic
            layout.addWidget(QtWidgets.QLabel(f"Content: {post['content']}"))
            layout.addWidget(QtWidgets.QLabel(f"Timestamp: {post['timestamp']}"))
            layout.addWidget(QtWidgets.QLabel(f"Likes: {len(post['likes'])}"))
            layout.addWidget(QtWidgets.QLabel(f"Dislikes: {len(post['dislikes'])}"))
            
            comment_label = QtWidgets.QLabel("Comments:")
            layout.addWidget(comment_label)
            for comment in post['comments']:
                comment_label = QtWidgets.QLabel(f"{comment['author']}: {comment['content']}")
                layout.addWidget(comment_label)

            buttons_layout = QtWidgets.QHBoxLayout()
            buttons_layout.addWidget(delete_button)
            buttons_layout.addWidget(comment_button)
            buttons_layout.addWidget(like_button)
            buttons_layout.addWidget(dislike_button)
            layout.addLayout(buttons_layout)

            self.posts_layout.addWidget(post_widget)

class ProfileDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ProfileDialog, self).__init__(parent)
        self.setWindowTitle("Profile Page")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(66, 183, 255, 255), stop:1 rgba(232, 43, 255, 255));
            border-radius: 15px;
            font-size: 16px;  /* Set default font size */
            color: white;
        """)

        self.profile_layout = QVBoxLayout()

        # Example profile data (replace with actual user data)
        self.username_label = QLabel(f"Username: {self.parent().current_user}")
        self.email_label = QLabel("Email:")
        self.email_value = QLineEdit(self.parent().user_email)
        self.bio_label = QLabel("Bio:")
        self.bio_value = QTextEdit(self.parent().user_bio)

        self.save_profile_button = QPushButton("Save Profile")
        self.save_profile_button.setStyleSheet("""
            background-color: black;
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
        """)
        self.save_profile_button.clicked.connect(self.save_profile)

        self.profile_layout.addWidget(self.username_label)
        self.profile_layout.addWidget(self.email_label)
        self.profile_layout.addWidget(self.email_value)
        self.profile_layout.addWidget(self.bio_label)
        self.profile_layout.addWidget(self.bio_value)
        self.profile_layout.addWidget(self.save_profile_button)

        self.setLayout(self.profile_layout)

    def save_profile(self):
        self.parent().user_email = self.email_value.text()
        self.parent().user_bio = self.bio_value.toPlainText()
        QMessageBox.information(self, "Profile", "Profile saved successfully!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
