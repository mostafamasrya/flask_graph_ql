from flask import Flask
from flask_graphql import GraphQLView
import graphene



app = Flask(__name__)




books_data = [
    {"title": "1984", "author": "George Orwell", "year_published": 1949},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year_published": 1960},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year_published": 1925},
]


#  GraphQL ObjectType, meaning it defines a structure for our data.
# this is our data schema
class Book(graphene.ObjectType):
    title = graphene.String()
    author = graphene.String()
    year_published = graphene.Int()



# we will create the QUERY view WHICH USED to return the data


class Query(graphene.ObjectType):
    books = graphene.List(Book)


    def resolve_books(self,info):
        return books_data



class AddBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        year_published = graphene.Int(required=True)

    book = graphene.Field(Book)

    def mutate(self,info,title,author,year_published):
        new_book = {"title": title, "author": author, "year_published": year_published}
        books_data.append(new_book)  # Add to our list
        return AddBook(book=new_book)



class Mutation(graphene.ObjectType):
    add_book = AddBook.Field()





schema = graphene.Schema(query=Query,mutation=Mutation)


app.add_url_rule(
    "/graphql",
    view_func = GraphQLView.as_view(
         "graphql",
         schema=schema,
         graphiql=True
    )
)


@app.route('/')
def home():
    return "Welcome to Flask with GraphQL!"

if __name__ == "__main__":
    app.run(debug=True)




    