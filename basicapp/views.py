from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import userinfo,Bookings,contact_us
from django.http import HttpResponse
from collections import deque, namedtuple

# Create your views here.
def index(request):
    return render(request,'TryCycle.html')

def register(request):

    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone_no=request.POST['phone_no']
        reg_no=request.POST['reg_no']
        room_no=request.POST['room_no']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1==password2:
            user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
            userinfos=userinfo(email=email,first_name=first_name,last_name=last_name,reg_no=reg_no,room_no=room_no,phone_no=phone_no)
            user.save() 
            userinfos.save()
            messages.info(request,'user created')
            return render(request,'Trycycle.html')
        else:
            messages.info(request,'Password does not match')
            return render(request,'Trycycle.html')
            
    else:    
        return render(request,'Trycycle.html')

def logout(request):
    auth.logout(request)
    return redirect('/') 

def login(request):
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid cedentials') 
            return redirect('login')   
    else:
        return render(request,'login.html')   

def fare(request):
        return render(request,'fare.html') 

def farecal(request):
    if request.method == 'POST':
    
        startpt=request.POST['startpth']    
        lastpt=request.POST['endpth']
        inf = float('inf')
        Edge = namedtuple('Edge', 'start, end, cost')


        def make_edge(start, end, cost=1):
            return Edge(start, end, cost)


        class Graph:
            def __init__(self, edges):
                wrong_edges = [i for i in edges if len(i) not in [2, 3]]
                if wrong_edges:
                    raise ValueError('Wrong edges data: {}'.format(wrong_edges))

                self.edges = [make_edge(*edge) for edge in edges]

            @property
            def vertices(self):
                return set(
                    sum(
                        ([edge.start, edge.end] for edge in self.edges), []
                    )
                )

            def get_node_pairs(self, n1, n2, both_ends=True):
                if both_ends:
                    node_pairs = [[n1, n2], [n2, n1]]
                else:
                    node_pairs = [[n1, n2]]
                return node_pairs

            def remove_edge(self, n1, n2, both_ends=True):
                node_pairs = self.get_node_pairs(n1, n2, both_ends)
                edges = self.edges[:]
                for edge in edges:
                    if [edge.start, edge.end] in node_pairs:
                        self.edges.remove(edge)

            def add_edge(self, n1, n2, cost=1, both_ends=True):
                node_pairs = self.get_node_pairs(n1, n2, both_ends)
                for edge in self.edges:
                    if [edge.start, edge.end] in node_pairs:
                        return ValueError('Edge {} {} already exists'.format(n1, n2))

                self.edges.append(Edge(start=n1, end=n2, cost=cost))
                if both_ends:
                    self.edges.append(Edge(start=n2, end=n1, cost=cost))

            @property
            def neighbours(self):
                neighbours = {vertex: set() for vertex in self.vertices}
                for edge in self.edges:
                    neighbours[edge.start].add((edge.end, edge.cost))

                return neighbours

            def dijkstra(self, source, dest):
                assert source in self.vertices, 'Such source node doesn\'t exist'
                distances = {vertex: inf for vertex in self.vertices}
                previous_vertices = {
                    vertex: None for vertex in self.vertices
                }
                distances[source] = 0
                vertices = self.vertices.copy()

                while vertices:
                    current_vertex = min(
                        vertices, key=lambda vertex: distances[vertex])
                    vertices.remove(current_vertex)
                    if distances[current_vertex] == inf:
                        break
                    for neighbour, cost in self.neighbours[current_vertex]:
                        alternative_route = distances[current_vertex] + cost
                        if alternative_route < distances[neighbour]:
                            distances[neighbour] = alternative_route
                            previous_vertices[neighbour] = current_vertex

                path, current_vertex = deque(), dest
                while previous_vertices[current_vertex] is not None:
                    path.appendleft(current_vertex)
                    current_vertex = previous_vertices[current_vertex]
                if path:
                    path.appendleft(current_vertex)
                return path

        graph = Graph([
            ("Main Building", "SMV", 3),  ("Main Building", "Technology Tower", 5),  ("Main Building", "Health Center", 3), ("SMV", "Technology Tower", 3),
            ("SMV","SJT", 10), ("Technology Tower", "SJT", 5), ("Technology Tower", "Health Center", 6),  ("SJT", "Men's Hostel", 10),
            ("Men's Hostel", "Health Center", 10)])

        graphdat=([
            ("Main Building", "SMV", 3),  ("Main Building", "Technology Tower", 5),  ("Main Building", "Health Center", 3), ("SMV", "Technology Tower", 3),
            ("SMV","SJT", 10), ("Technology Tower", "SJT", 5), ("Technology Tower", "Health Center", 6),  ("SJT", "Men's Hostel", 10),
            ("Men's Hostel", "Health Center", 10)])
        tot=0
        tab=graph.dijkstra(startpt,lastpt)
        for i in range(0,len(tab)-1):
            for j in graphdat:
                if(tab[i]==j[0] and tab[i+1]==j[1]):
                    tot=tot+j[2]
            
        return render(request,'fare.html',{'fare_tot':'Your total fare would be '+str(tot)+'rs'}) 

def rent_now(request):
    if request.method == 'POST':
        username = None
        username = request.user.username
        date=request.POST['date']
        check=request.POST['check']
        end=request.POST['end']
        cht=request.POST['cht']

            
        booked=Bookings(user=username,date=date,check=check,end=end,cht=cht)
        booked.save()
        return render(request,'Trycycle.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        feed=request.POST['feed']
        contacted=contact_us(name=name,email=email,subject=subject,feed=feed)

        contacted.save()
        return render(request,'Trycycle.html')

def mybookings(request):
    booking_list = Bookings.objects.order_by('id')
    date_dict = {'bookings':booking_list}
    return render(request,'mybookings.html',context=date_dict)
        