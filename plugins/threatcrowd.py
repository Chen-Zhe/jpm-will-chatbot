from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests, json
import numpy as np
from sklearn import manifold
import random


class threatcrowdemail(WillPlugin):

    @hear("~email(-tc)? (?P<input>.*)")
    def check_email(self, message, input):

        input_list = [input_item.strip() for input_item in input.split(',')]
        for email in input_list:
            result = requests.get("https://www.threatcrowd.org/searchApi/v2/email/report/", params={"email": email})
            j = json.loads(result.text)

            if j['response_code']=="0":

                response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".",
                                                                                   "[.]") + "\nTotal number of Domains: 0"

            else:
                count = len(j['domains'])

                end = 5
                if len(j["domains"]) < 5:
                    end = len(j["domains"])
                domainlist = ", ".join(j["domains"][0:end])

                if count >= 3:
                    K = 3

                    # compute distance matrix for all domains
                    similarity = []

                    # compute distance between two domains
                    def domain_similarity(s1, s2):

                        if len(s1) > len(s2):
                            s1, s2 = s2, s1
                        distances = range(len(s1) + 1)

                        for i2, c2 in enumerate(s2):
                            distances_ = [i2 + 1]
                            for i1, c1 in enumerate(s1):
                                if c1 == c2:
                                    distances_.append(distances[i1])
                                else:
                                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
                            distances = distances_
                        return distances[-1]

                    # clustering all points according to given centroid
                    def cluster_points(X, mu):
                        clusters = {}
                        for x in X:
                            bestmukey = min([(i[0], np.linalg.norm(x - mu[i[0]])) \
                                             for i in enumerate(mu)], key=lambda t: t[1])[0]
                            try:
                                clusters[bestmukey].append(x)
                            except KeyError:
                                clusters[bestmukey] = [x]
                        return clusters

                    # relocate centroids
                    def reevaluate_centers(mu, clusters):
                        newmu = []
                        keys = sorted(clusters.keys())
                        for key in keys:
                            newmu.append(np.mean(clusters[key], axis=0))
                        return newmu

                    # check convergence of centroids
                    def has_converged(mu, oldmu):
                        return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

                    # find stable centroids
                    def find_centroids(X, k):
                        # Initialize to K random centers
                        oldmu = random.sample(X, k)
                        mu = random.sample(X, k)
                        while not has_converged(mu, oldmu):
                            oldmu = mu
                            # Assign all points in X to clusters
                            clusters = cluster_points(X, mu)
                            # Reevaluate centers
                            mu = reevaluate_centers(oldmu, clusters)
                        return (mu, clusters)

                    # Euclidean distance
                    def Eu_distance(P1, P2):
                        dist = np.sqrt(pow((P1[0] - P2[0]), 2) + pow((P1[1] - P2[1]), 2))
                        return dist

                    # Find corresponding domain name for given coordinates
                    def find_domain(coordinates):
                        for m in range(0, count):
                            if coordinates[0] == coords[m][0] and coordinates[1] == coords[m][1]:
                                return str(j['domains'][m])

                    def find_result(X, k):
                        (M, C) = find_centroids(X, k)

                        # change to integer coordinates
                        for l in range(0, k):
                            for point_index in range(0, len(C[l])):
                                C[l][point_index] = [int(C[l][point_index][0]), int(C[l][point_index][1]), find_domain(C[l][point_index])]

                        # find acutal center
                        for i in range(0, k):
                            dis_array = []
                            for point in C[i]:
                                dis_array.append(Eu_distance(point, M[i]))
                            index = dis_array.index(min(dis_array))
                            # Store center
                            center_point = C[i].pop(index)
                            C[i].insert(0, center_point)
                            C[str(i)] = C.pop(i)

                        return C

                    for count_index1 in range(0, count):
                        tmp = []
                        for count_index2 in range(0, count):
                            if count_index1 == count_index2:
                                simi = 0
                            elif count_index1 < count_index2:
                                simi = domain_similarity(j['domains'][count_index1], j['domains'][count_index2])
                            else:
                                simi = similarity[count_index2][count_index1]
                            tmp.append(simi)
                        similarity.append(tmp)

                    # scale the distance matrix
                    adist = np.array(similarity)
                    adist = adist * 10

                    # compute coordinates matrix
                    mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
                    results = mds.fit(adist)
                    coords = results.embedding_

                    output_data = find_result(coords, K)

                    response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".",
                                                                                   "[.]") + "\nTotal number of domains: " + str(
                        count) + "\n" + "Most recently registered domains: " + domainlist +"\nurl: localhost:9000/visualize/123"

                    self.save("123", json.dumps(output_data))


                else:
                    response = "ThreatCrowd Scan Result\n" + "Email: " + email.replace(".",
                                                                                   "[.]") + "\nTotal number of domains: " + str(
                        count) + "\n" + "Most recently registered domains: " + domainlist

            self.reply(message, response)


